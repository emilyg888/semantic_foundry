from __future__ import annotations

from pathlib import Path

from semantic_foundry.review.service import (
    add_issue,
    approve_asset,
    load_package_review_state,
    publish_review_package,
    reject_asset,
    resolve_issue,
    update_owner,
)


DEFAULT_PACKAGE_PATH = "outputs/business_banking_fraud_detection"


def run_dashboard() -> None:
    import streamlit as st

    st.set_page_config(page_title="Semantic_Foundry Review Cockpit", layout="wide")
    st.markdown(
        """
        <style>
        button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] p {
            font-size: 1.15rem;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("Semantic_Foundry Review Cockpit")

    package_input = st.sidebar.text_input("Package path", value=DEFAULT_PACKAGE_PATH)
    package_path = Path(package_input).expanduser()
    if not package_path.exists():
        st.error(f"Package path does not exist: {package_path}")
        return

    state = load_package_review_state(package_path)
    st.sidebar.caption(f"Loaded package: {package_path}")
    st.sidebar.markdown("**Certification result**")
    st.sidebar.write(state.gate.result)
    st.sidebar.markdown("**Validation status**")
    st.sidebar.write(state.gate.validation_status)

    summary_tab, assets_tab, issues_tab, publish_tab = st.tabs(["Summary", "Assets", "Issues", "Publish"])

    with summary_tab:
        st.subheader("Certification Summary")
        st.write(
            {
                "result": state.gate.result,
                "validation_status": state.gate.validation_status,
                "asset_stage_counts": state.gate.asset_stage_counts,
                "blockers": state.gate.blockers,
            }
        )
        st.subheader("Requirements")
        for requirement in state.gate.requirements:
            label = "Passed" if requirement.passed else "Pending"
            st.write(f"- `{requirement.name}`: {label} — {requirement.detail}")

    with assets_tab:
        st.subheader("Review Assets")
        asset_type = st.selectbox(
            "Asset type",
            options=["glossary", "entities", "signals", "predictions", "metrics"],
        )
        assets = [asset for asset in state.review_assets if asset.asset_type == asset_type]
        if not assets:
            st.info("No reviewable assets found for this type.")
        else:
            selected_label = st.selectbox(
                "Asset",
                options=[f"{asset.asset_id} [{asset.status}]" for asset in assets],
            )
            selected_asset = next(asset for asset in assets if f"{asset.asset_id} [{asset.status}]" == selected_label)
            widget_prefix = f"{selected_asset.asset_type}-{selected_asset.asset_id}"
            st.write(
                {
                    "asset_id": selected_asset.asset_id,
                    "display_name": selected_asset.display_name,
                    "owner": selected_asset.owner,
                    "status": selected_asset.status,
                    "source_references": selected_asset.source_references,
                }
            )

            reviewer = st.text_input("Reviewer", value="Business Reviewer", key=f"{widget_prefix}-reviewer")
            owner = st.text_input("Owner", value=selected_asset.owner, key=f"{widget_prefix}-owner")
            comments = st.text_area("Comments", value="", key=f"{widget_prefix}-comments")
            blocking_issue = st.checkbox(
                "Create blocking issue on rejection",
                value=True,
                key=f"{widget_prefix}-blocking",
            )
            severity = st.selectbox(
                "Issue severity",
                options=["low", "medium", "high", "critical"],
                index=2,
                key=f"{widget_prefix}-severity",
            )
            action_col1, action_col2, action_col3 = st.columns(3)
            with action_col1:
                with st.form(f"{widget_prefix}-approve-form"):
                    approve_clicked = st.form_submit_button("Approve", use_container_width=True, type="primary")
            with action_col2:
                with st.form(f"{widget_prefix}-reject-form"):
                    reject_clicked = st.form_submit_button("Reject", use_container_width=True)
            with action_col3:
                with st.form(f"{widget_prefix}-owner-form"):
                    owner_clicked = st.form_submit_button("Update owner", use_container_width=True)

            try:
                if owner_clicked:
                    update_owner(package_path, selected_asset.asset_type, selected_asset.asset_id, owner)
                    st.success("Owner updated.")
                    st.rerun()
                if approve_clicked:
                    approve_asset(package_path, selected_asset.asset_type, selected_asset.asset_id, reviewer, comments)
                    st.success("Asset approved and package refreshed.")
                    st.rerun()
                if reject_clicked:
                    reject_asset(
                        package_path,
                        selected_asset.asset_type,
                        selected_asset.asset_id,
                        reviewer,
                        comments or f"{selected_asset.asset_id} requires further review.",
                        blocking=blocking_issue,
                        severity=severity,
                    )
                    st.warning("Asset rejected and issue captured.")
                    st.rerun()
            except Exception as exc:
                st.error(f"Asset action failed: {exc}")

    with issues_tab:
        st.subheader("Issue Register")
        for issue in state.issues:
            status = str(issue.get("status", "open"))
            st.write(
                {
                    "asset": issue.get("asset"),
                    "severity": issue.get("severity"),
                    "blocking": issue.get("blocking"),
                    "status": status,
                    "issue": issue.get("issue"),
                }
            )
            if status != "resolved":
                button_key = f"resolve-{issue.get('asset')}-{issue.get('issue')}"
                if st.button(f"Resolve: {issue.get('asset')} / {issue.get('issue')}", key=button_key):
                    resolve_issue(package_path, str(issue.get("issue")), resolver="Review Cockpit", resolution_note="Resolved in review cockpit")
                    st.success("Issue resolved and certification artefacts refreshed.")
                    st.rerun()

        st.subheader("Capture New Issue")
        with st.form("new-issue"):
            issue_asset = st.text_input("Asset", value="certified_transaction")
            issue_text = st.text_area("Issue")
            issue_severity = st.selectbox("Severity", options=["low", "medium", "high", "critical"], index=2)
            issue_blocking = st.checkbox("Blocking", value=True)
            issue_reporter = st.text_input("Reported by", value="Review Cockpit")
            issue_submit = st.form_submit_button("Add issue")
        if issue_submit and issue_text.strip():
            add_issue(package_path, issue_asset, issue_text.strip(), issue_severity, issue_blocking, issue_reporter)
            st.success("Issue added and certification artefacts refreshed.")
            st.rerun()

    with publish_tab:
        st.subheader("Publish Package")
        st.write("Publishing refreshes the certification report, semantic manifest, and publish log using the latest review state.")
        publisher = st.text_input("Publisher", value="Review Cockpit", key="publish-publisher")
        notes = st.text_area("Publish notes", value="", key="publish-notes")
        publish_clicked = st.button("Publish package", key="publish-package-button", type="primary")
        try:
            if publish_clicked:
                gate = publish_review_package(package_path, publisher=publisher, notes=notes)
                st.success(f"Package published with certification result: {gate.result}")
                st.rerun()
        except Exception as exc:
            st.error(f"Publish failed: {exc}")
