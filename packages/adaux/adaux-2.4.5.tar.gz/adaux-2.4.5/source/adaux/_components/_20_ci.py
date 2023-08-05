# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
# pylint: disable=too-many-lines
import os
import typing as tp

from .._logging import logger
from .._proto_namespace import _ProtoNamespace
from .._util import ApiRequestCommunicator
from ._00_extra_level import ExtraLevel
from ._03_meta import MetaMixin
from ._18_payload import PayloadMixin


class CiMixin(PayloadMixin, MetaMixin):
    # pylint: disable=unused-private-member
    @classmethod
    def __keys(cls) -> tp.Tuple[str, ...]:
        return ("mechanism", "docker_image", "runner", "trigger", "use_adaux_img")

    def templated(self, negative_default: bool = False) -> None:
        super().templated(negative_default)
        self.auxcon.ci = _ProtoNamespace(trigger=_ProtoNamespace())
        data = self.auxcon.ci.trigger
        data["+push"] = {
            "-openmr": {
                "-release": {"pre-commit": None},
                "+release": {
                    "+gitlab": {
                        "gitlab-release": None,
                        "pkg-gitlab": None,
                    }
                },
            }
        }
        data["+mr"] = {
            "+draft": {
                "pre-commit": None,
            },
            "-draft": {
                "pre-commit-all": None,
            },
            "+release": {
                "check-release-notes": None,
            },
        }

        if self.is_enabled("pytest"):
            data["+push"]["-openmr"]["-release"]["pytest"] = None
            data["+mr"]["+draft"]["pytest"] = None
            if self.is_enabled("coverage"):
                data["+mr"]["-draft"].update(
                    {
                        "-vip": {
                            "pytest-mr": None,
                        },
                        "+vip": {
                            "pytest-cov-mr": None,
                        },
                    }
                )
            else:
                data["+mr"]["-draft"]["pytest-mr"] = None

        if self.is_enabled("docs"):
            data["+mr"]["-draft"]["+release"] = {"docs": None}
            data["+push"]["-openmr"]["+release"]["docs"] = None

    def update_to_template(self, tpl: _ProtoNamespace, full: _ProtoNamespace) -> None:
        super().update_to_template(tpl, full)

        with self.extra(ExtraLevel.HYDRATED) as auxe:  # type: ignore
            valid_payloads = auxe.payload.lookup.all_keys()

        added = []

        def deep_add(trig_chain: str, obj: tp.Any) -> None:
            last_key = trig_chain.rsplit(".", 1)[1]
            if last_key.startswith("+") or last_key.startswith("-"):
                for key, val in obj.items():
                    deep_add(trig_chain + "." + key, val)
            else:
                added.append(trig_chain)

        def deep_merge(
            tpl: tp.Optional[_ProtoNamespace],
            user: tp.Optional[_ProtoNamespace],
            trig_chain: str = "ci.trigger",
        ) -> tp.Optional[_ProtoNamespace]:
            if tpl is None and user is None:
                return None
            if tpl is None:
                return user
            if user is None:
                deep_add(trig_chain, tpl)
                return tpl
            res = _ProtoNamespace()
            all_keys = list(tpl.keys())
            all_keys += [x for x in user.keys() if x not in all_keys]

            for key in all_keys:
                res[key] = deep_merge(
                    tpl.get(key), user.get(key), trig_chain=trig_chain + "." + key
                )
            return res

        new_trigger = deep_merge(tpl.ci.trigger, self.auxf.ci.trigger)

        removed = []

        def deep_remove(
            trigger: tp.Optional[_ProtoNamespace], trig_chain: str = "ci.trigger"
        ) -> None:
            if trigger is None:
                return
            for key, val in list(trigger.items()):
                if key.startswith("+") or key.startswith("-"):
                    deep_remove(val, trig_chain=trig_chain + "." + key)
                    if not trigger[key]:
                        del trigger[key]
                elif key not in valid_payloads:
                    del trigger[key]
                    removed.append(f"{trig_chain}.{key}")

        deep_remove(new_trigger)
        overlap = set(added) & set(removed)
        if overlap:
            logger.warning("overlap (added and removed) in ci.trigger: %s", overlap)
        for add in added:
            if add not in overlap:
                self._print(f"added  {add}", fg="green")
        for rem in removed:
            if rem not in overlap:
                self._print(f"removed {rem}", fg="red")
        self.auxf.ci.trigger = new_trigger

    def demodata(self) -> None:
        super().demodata()
        self.auxcon.ci.runner = "dind-cached"
        self.auxcon.ci.mechanism = "mixed"

    def formatted(self) -> None:
        super().formatted()
        self._copy_keys_over(self.__keys(), "ci")

        for key in ["trigger"]:
            self._to_proto_ns("ci", key, iter_mapping=True)

    def defaulted(self) -> None:
        super().defaulted()
        self.auxd.setdefault("ci", _ProtoNamespace())
        data = self.auxd.ci

        data.setdefault("mechanism", "monolith")
        data.setdefault("runner", "normal")
        data.setdefault("docker_image", self.versions.ci_docker_image)
        data.setdefault("trigger", _ProtoNamespace())
        data.setdefault("use_adaux_img", True)
        assert data.trigger is not None
        assert data.mechanism in ["monolith"]
        assert data.runner in ["dind-cached", "normal"]

    def enriched(self) -> None:
        super().enriched()
        data = self.auxe.ci

        rule_used = _ProtoNamespace(
            mr=False,
            web=False,
            pipeline=False,
            schedule=False,
        )
        for reason in self._get_trigger_combos():
            for key in ["push", "push_no_mr"] + list(rule_used):
                if key in ["push", "push_no_mr"]:
                    if "+push" in reason:
                        rule_used.setdefault("push", False)
                        rule_used.setdefault("push_no_mr", True)
                        if "-openmr" not in reason:
                            rule_used["push_no_mr"] &= False
                            rule_used["push"] |= True
                else:
                    rule_used[key] |= f"+{key}" in reason

        data.used_rules = [key for key, val in rule_used.items() if val]

    def run_ci(self, trigger_str: str, dry: bool = False) -> int:
        if trigger_str == "gitlab":
            triggers = self._triggers_from_gitlab_ci()
        else:
            triggers = self._triggers_from_str(trigger_str)

        # get the payload_names
        payload_names = self._get_payload_names(triggers)

        self._print(f"triggers: {', '.join(triggers)}", fg="cyan")

        if not payload_names:
            self._print("no payloads selected", fg="yellow")
            return 0
        payloads = [self.auxh.payload.lookup[x] for x in payload_names]
        success = self.payload_run(*payloads, force=False, dry=dry)
        if success:
            if "+draft" in triggers:
                return 42
            return 0
        return 1

    def _triggers_from_gitlab_ci(self) -> tp.Sequence[str]:
        triggers = []

        def env(key: str) -> str:
            return os.environ.get(key, "")

        gitlab2adaux = {
            "push": "+push",
            "merge_request_event": "+mr",
            "web": "+web",
            "pipeline": "+pipeline",
            "schedule": "+schedule",
        }
        source_trigger = gitlab2adaux[env("CI_PIPELINE_SOURCE")]
        triggers.append(source_trigger)

        if env("CI_COMMIT_TAG") != "":
            assert source_trigger == "+push"
            source_trigger = "+tag"
        if env("CI_OPEN_MERGE_REQUESTS") != "":
            triggers.append("+openmr")
            # we dont care abound env("CI_OPEN_MERGE_REQUESTS") in push
            # draft is only an option for mr lines

        mr_iid = env("CI_MERGE_REQUEST_IID")
        if mr_iid != "":
            try:
                resp = self.get_mr_status(mr_iid)
                if resp["draft"]:
                    triggers.append("+draft")
                    logger.info("merge request %s is a draft", mr_iid)
                else:
                    logger.info("merge request %s is NOT a draft", mr_iid)
            except RuntimeError as err:
                self._print(
                    f"could not access gitlab api for checking mr draft ({err.args[0]})",
                    fg="red",
                )

        if source_trigger == "+push":
            branch = env("CI_COMMIT_BRANCH")
        elif source_trigger == "+mr":
            branch = env("CI_MERGE_REQUEST_TARGET_BRANCH_NAME")

        gitlab = self.auxh.gitlab
        if branch in gitlab.vip_branches:
            triggers.append("+vip")
        if branch == gitlab.default_branch:
            triggers.append("+default")
        if branch == gitlab.release_branch:
            triggers.append("+release")

        branch_trigger = f"+{branch}"
        if branch_trigger not in triggers:
            triggers.append(branch_trigger)

        triggers.append("+gitlab")
        return triggers

    def get_mr_status(self, mr_iid: str) -> tp.Dict[str, tp.Any]:
        coord = [
            "projects",
            os.environ["CI_PROJECT_ID"],
            "merge_requests",
            mr_iid,
        ]
        api = ApiRequestCommunicator()
        token = os.environ["GITLAB_READ_API"]
        api.headers = {"PRIVATE-TOKEN": token}
        api.base_url = "https://" + os.environ["CI_SERVER_HOST"]
        return api.api_request(*coord)  # type: ignore

    def _triggers_from_str(self, trigger_str: str) -> tp.Sequence[str]:
        if trigger_str[0] not in "+-":
            trigger_str = f"+{trigger_str}"

        triggers = []
        old = 0
        for i, char in enumerate(trigger_str):
            if char in "+-":
                triggers.append(trigger_str[old:i])
                old = i
        triggers.append(trigger_str[old:])
        waste = triggers.pop(0)
        assert waste == ""
        return triggers

    def _get_payload_names(self, triggers: tp.Sequence[str]) -> tp.Sequence[str]:
        res = []
        for payload_name, reason in self._get_payload_names_and_reason(triggers):
            logger.info("%s included due to %s", payload_name, "".join(reason))
            res.append(payload_name)
        return res

    def _get_payload_names_and_reason(
        self, triggers: tp.Sequence[str], collect_all: bool = False
    ) -> tp.Sequence[tp.Tuple[str, tp.Tuple[str, ...]]]:
        payload_names_reason = []
        data = self.auxe.ci.trigger

        def dig(data: _ProtoNamespace, reason: tp.Tuple[str, ...]) -> None:
            for key, val in data.items():
                if key.startswith("-"):
                    pos_key = key.replace("-", "+")
                    if pos_key not in triggers or collect_all:
                        dig(val, reason + (key,))
                elif key.startswith("+"):
                    if key in triggers or collect_all:
                        dig(val, reason + (key,))
                else:
                    payload_names_reason.append((key, reason))

        dig(data, tuple())

        return payload_names_reason

    def _get_trigger_combos(self) -> tp.Sequence[tp.Tuple[str, ...]]:
        reasons = set()
        for _, reason in self._get_payload_names_and_reason([], collect_all=True):
            reasons.add(reason)
        return list(reasons)

    def bake(self) -> None:  # pylint: disable=too-many-branches,too-many-locals
        super().bake()
        data = self.auxe.ci
        base_files = ["00-main.yml", "01-rules.yml"]
        assert data.mechanism == "monolith"

        for filename in base_files:
            self.bake_file(f"CI/{filename}")
