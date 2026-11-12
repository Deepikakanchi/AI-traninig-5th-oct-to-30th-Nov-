import asyncio
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Never

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agent_framework import (
    Agent,
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    executor,
    handler,
    response_handler,
)
from agent_framework.openai import OpenAIChatClient


BASE_DIR = Path(__file__).resolve().parent
RETURNS_FILE = BASE_DIR / "returns.json"
load_dotenv(BASE_DIR / ".env")


# Task 5: Keep the full request and prompt while the workflow waits for a manager.
@dataclass
class ManagerApprovalRequest:
    request: dict[str, Any]
    prompt: str


# Task 5: Pause for human approval, validate the response, and resume with context.
class ApprovalGateway(Executor):
    def __init__(self) -> None:
        super().__init__(id="approval_gateway")

    @handler
    async def review(
        self,
        request: dict[str, Any],
        ctx: WorkflowContext[dict[str, Any]],
    ) -> None:
        business = evaluate_business_rules(
            request,
            risk_level=request.get("risk_level", "HIGH"),
        )
        reviewed_request = {**request, **business}

        if business["business_decision"] == "AUTO_APPROVE":
            reviewed_request["decision"] = "AUTO_APPROVED"
            reviewed_request["decision_by"] = "Return policy"
            await ctx.send_message(reviewed_request)
            return

        failed_checks = ", ".join(business["failed_checks"]) or "None"
        prompt = (
            f"Request ID: {request.get('request_id')}\n"
            f"Item: {request.get('product')}\n"
            f"Amount: INR {request.get('amount_inr'):,}\n"
            f"Eligibility issues: {failed_checks}\n"
            f"Risk assessment: {request.get('risk_level', 'HIGH')} - "
            f"{request.get('risk_summary', 'Risk assessment unavailable')}\n"
            "Type approve or reject: "
        )
        await ctx.request_info(
            request_data=ManagerApprovalRequest(
                request=reviewed_request,
                prompt=prompt,
            ),
            response_type=str,
        )

    @response_handler
    async def on_manager_decision(
        self,
        original_request: ManagerApprovalRequest,
        response: str,
        ctx: WorkflowContext[dict[str, Any]],
    ) -> None:
        decision = response.strip().lower()
        if decision not in {"approve", "reject"}:
            raise ValueError("Manager decision must be 'approve' or 'reject'.")

        request = dict(original_request.request)
        request["decision"] = (
            "MANAGER_APPROVED" if decision == "approve" else "MANAGER_REJECTED"
        )
        request["decision_by"] = "Human manager"
        request["manager_decision"] = decision
        await ctx.send_message(request)


# Task 1: Load all customer return records dynamically from returns.json.
def load_return_requests(file_path: str | Path = RETURNS_FILE) -> list[dict[str, Any]]:
    """Load customer return requests from JSON."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError(
            f"Expected a list of records in {path}, found {type(records).__name__}"
        )

    return records


# Task 3: Apply deterministic risk checks; HIGH risk blocks automatic approval.
def assess_risk_level(request: dict[str, Any]) -> str:
    """Deterministic risk scoring used before AI-generated suggestions are considered."""
    risk_flags = []

    if request.get("amount_inr", 0) >= 25_000:
        risk_flags.append("high value")
    if request.get("previous_returns_90_days", 0) >= 3:
        risk_flags.append("frequent prior returns")
    if not request.get("invoice_available", False):
        risk_flags.append("missing invoice")
    if request.get("item_condition") == "DAMAGED" and not request.get("photo_evidence_available", False):
        risk_flags.append("damaged item without photo evidence")
    if request.get("days_since_delivery", 0) > 30:
        risk_flags.append("outside return window")

    if risk_flags:
        return "HIGH"

    if request.get("previous_returns_90_days", 0) >= 2 or request.get("amount_inr", 0) >= 15_000:
        return "MEDIUM"

    return "LOW"


# Task 3: Enforce every automatic-approval condition in Python.
def evaluate_business_rules(
    request: dict[str, Any],
    risk_level: str | None = None,
) -> dict[str, Any]:
    """Apply the required return policy as deterministic Python checks."""
    assessed_risk = risk_level or assess_risk_level(request)
    amount_ok = request.get("amount_inr", 0) < 25_000
    within_window = request.get("days_since_delivery", 0) <= 30
    invoice_ok = bool(request.get("invoice_available", False))
    condition = request.get("item_condition", "")
    damaged_with_photo = (
        condition == "DAMAGED" and bool(request.get("photo_evidence_available", False))
    )
    unopened_ok = condition == "UNOPENED"
    item_condition_ok = unopened_ok or damaged_with_photo
    previous_returns_ok = request.get("previous_returns_90_days", 0) < 3
    risk_ok = assessed_risk != "HIGH"

    checks = {
        "amount_under_25000": amount_ok,
        "within_30_days": within_window,
        "invoice_available": invoice_ok,
        "valid_item_condition": item_condition_ok,
        "fewer_than_three_previous_returns": previous_returns_ok,
        "risk_not_high": risk_ok,
    }

    auto_approve = all(checks.values())
    failed = [name for name, ok in checks.items() if not ok]

    return {
        "request_id": request.get("request_id"),
        "order_id": request.get("order_id"),
        "product": request.get("product"),
        "request_type": request.get("request_type"),
        "business_decision": "AUTO_APPROVE" if auto_approve else "ESCALATE_FOR_HUMAN_REVIEW",
        "risk_level": assessed_risk,
        "checks": checks,
        "failed_checks": failed,
    }


def build_final_output(
    request: dict[str, Any],
    decision: str,
    eligibility: str,
    eligibility_explanation: str,
    risk_level: str,
    risk_summary: str,
    customer_message: str,
) -> dict[str, Any]:
    """Build the consistent Task 6 response for either execution mode."""
    return {
        "request_id": request["request_id"],
        "order_id": request["order_id"],
        "product": request["product"],
        "requested_amount_inr": request["amount_inr"],
        "eligibility_findings": {
            "agent_assessment": eligibility,
            "explanation": eligibility_explanation,
            "policy_issues": request.get("failed_checks", []),
        },
        "risk_assessment": {
            "level": risk_level,
            "summary": risk_summary,
        },
        "approval_route": "Automatic" if decision == "AUTO_APPROVED" else "Human Review",
        "final_decision": decision,
        "customer_communication_draft": customer_message,
        "simulation_notice": (
            "Simulation only. No payments were processed, no messages were sent, "
            "and no replacements were initiated."
        ),
    }


# Task 1 / Task 3: Create a policy-based summary when AI credentials are not configured.
def evaluate_request(request: dict[str, Any]) -> dict[str, Any]:
    """Deterministic policy baseline used when AI config is unavailable."""
    business = evaluate_business_rules(request)
    flags: list[str] = []

    if not business["checks"]["amount_under_25000"]:
        flags.append("amount is 25000 or above")
    if not business["checks"]["within_30_days"]:
        flags.append("outside return window")
    if not business["checks"]["invoice_available"]:
        flags.append("missing invoice")
    if not business["checks"]["valid_item_condition"]:
        flags.append("item is not valid for auto approval")
    if not business["checks"]["fewer_than_three_previous_returns"]:
        flags.append("three or more returns in 90 days")
    if not business["checks"]["risk_not_high"]:
        flags.append("high-risk concern")

    decision = "READY_FOR_PROCESSING" if business["business_decision"] == "AUTO_APPROVE" else "MANUAL_REVIEW"

    return {
        "request_id": request.get("request_id"),
        "order_id": request.get("order_id"),
        "product": request.get("product"),
        "request_type": request.get("request_type"),
        "amount_inr": request.get("amount_inr"),
        "days_since_delivery": request.get("days_since_delivery"),
        "item_condition": request.get("item_condition"),
        "decision": decision,
        "business_decision": business["business_decision"],
        "risk_level": business["risk_level"],
        "flags": flags,
    }


# Task 1: Process the dynamically loaded records one by one.
def process_requests(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Process all requests and return a summary per record."""
    return [evaluate_request(record) for record in records]


def print_summary(processed: list[dict[str, Any]]) -> None:
    total_amount = sum(item["amount_inr"] for item in processed)
    ready = sum(1 for item in processed if item["decision"] == "READY_FOR_PROCESSING")
    manual_review = sum(1 for item in processed if item["decision"] == "MANUAL_REVIEW")

    print(f"Loaded {len(processed)} return requests")
    print(f"Total refund/replacement value: INR {total_amount:,}")
    print(f"Ready for processing: {ready}")
    print(f"Manual review required: {manual_review}")
    print("\nDetailed request review:\n")

    for item in processed:
        print(
            f"{item['request_id']} | {item['product']} | "
            f"{item['request_type']} | {item['item_condition']} | "
            f"INR {item['amount_inr']:,} | {item['business_decision']} | {item['risk_level']}"
        )
        if item["flags"]:
            print(f"  Issues: {', '.join(item['flags'])}")


# Task 2 / Task 4: Define the specialized agents and connect their executors as a graph.
def build_workflow(chat_client: OpenAIChatClient):
    """Create the eligibility → risk → approval → customer response workflow."""

    # Task 2: Agent 1 reviews eligibility and explains exceptions.
    eligibility_agent = Agent(
        client=chat_client,
        name="EligibilityAgent",
        instructions=(
            "Review the return request against the company's return policy. "
            "Use only the supplied facts. "
            "Reply with exactly one of these labels: ELIGIBLE, NOT_ELIGIBLE, or MANUAL_REVIEW. "
            "Then provide a short explanation of the decision and any exception notes."
        ),
    )

    # Task 2: Agent 2 assesses frequency, missing evidence, and high-value risk.
    risk_agent = Agent(
        client=chat_client,
        name="RiskAgent",
        instructions=(
            "Assess return request risk using only the provided request data. "
            "Identify unusual return frequency, missing evidence, and high-value items. "
            "Reply with one of LOW, MEDIUM, or HIGH followed by a brief justification."
        ),
    )

    # Task 2: Agent 3 drafts a customer response without claiming completion.
    response_agent = Agent(
        client=chat_client,
        name="CustomerResponseAgent",
        instructions=(
            "Draft a concise, polite customer-facing message based only on the supplied final decision. "
            "Never change or override that decision. Do not claim a refund or replacement is completed, "
            "and do not claim that any real payment, message, or replacement action has occurred. "
            "This is a simulation."
        ),
    )

    # Task 4: Pass the original request plus eligibility findings to the next executor.
    @executor(id="eligibility_check")
    async def eligibility_check(
        request: dict,
        ctx: WorkflowContext[dict],
    ) -> None:
        result = await eligibility_agent.run(
            "Review this return request against policy:\n" + json.dumps(request, ensure_ascii=False)
        )

        decision = result.text.strip().upper().split()[0].strip("*#:`.,")
        if decision not in {"ELIGIBLE", "NOT_ELIGIBLE", "MANUAL_REVIEW"}:
            decision = "MANUAL_REVIEW"

        await ctx.send_message({
            **request,
            "eligibility_decision": decision,
            "eligibility_reason": result.text.strip(),
        })

    # Task 4: Add the risk result while preserving all request and eligibility fields.
    @executor(id="risk_assessment")
    async def risk_assessment(
        request: dict,
        ctx: WorkflowContext[dict],
    ) -> None:
        result = await risk_agent.run(
            "Assess this return request for risk:\n" + json.dumps(request, ensure_ascii=False)
        )

        response = result.text.strip()
        risk_label = response.upper().split()[0].strip("*#:`.,")
        agent_risk = risk_label if risk_label in {"LOW", "MEDIUM", "HIGH"} else "HIGH"

        # A deterministic risk rule or an AI-identified HIGH concern must
        # prevent automatic approval.
        deterministic_risk = assess_risk_level(request)
        risk = (
            "HIGH"
            if "HIGH" in {agent_risk, deterministic_risk}
            else "MEDIUM"
            if "MEDIUM" in {agent_risk, deterministic_risk}
            else "LOW"
        )

        await ctx.send_message({
            **request,
            "risk_level": risk,
            "risk_summary": response,
        })

    # Task 6: Emit one structured simulation record with decision and customer draft.
    @executor(id="customer_response")
    async def customer_response(
        request: dict,
        ctx: WorkflowContext[Never, str],
    ) -> None:
        eligibility = request.get("eligibility_decision", "MANUAL_REVIEW")
        decision = request.get("decision", request["business_decision"])
        risk_level = request["risk_level"]

        if decision == "MANAGER_REJECTED":
            customer_message = (
                f"Your {request['request_type'].lower()} request for {request['product']} "
                "was reviewed and declined by a manager. This is a simulation; "
                "no refund or replacement has been processed."
            )
        else:
            result = await response_agent.run(
                "Draft a customer communication for this exact final decision; do not change it. "
                "State that the request is approved for the next processing step, not that it is completed. "
                "Mention that this is a simulation and no real payment or replacement action has occurred.\n"
                + json.dumps(request, ensure_ascii=False)
            )
            customer_message = result.text.strip()

        final_output = build_final_output(
            request=request,
            decision=decision,
            eligibility=eligibility,
            eligibility_explanation=request.get("eligibility_reason", ""),
            risk_level=risk_level,
            risk_summary=request.get("risk_summary", ""),
            customer_message=customer_message,
        )
        await ctx.yield_output(json.dumps(final_output, ensure_ascii=False, indent=2))

    # Task 4: Graph path: Eligibility -> Risk -> Approval Gateway -> Customer Response.
    approval_gateway = ApprovalGateway()
    workflow = (
        WorkflowBuilder(start_executor=eligibility_check)
        .add_edge(eligibility_check, risk_assessment)
        .add_edge(risk_assessment, approval_gateway)
        .add_edge(approval_gateway, customer_response)
        .build()
    )

    return workflow


# Task 5: Stream workflow events, prompt the manager, and resume paused workflow runs.
async def run_one(workflow: Any, request: dict[str, Any]) -> None:
    """Run a workflow, collect manager decisions, and resume any paused runs."""
    first_run = True
    responses: dict[str, str] | None = None

    while True:
        stream = (
            workflow.run(request, stream=True)
            if first_run
            else workflow.run(stream=True, responses=responses)
        )
        first_run = False
        pending: dict[str, ManagerApprovalRequest] = {}
        outputs: list[str] = []

        async for event in stream:
            if event.type == "request_info":
                pending[event.request_id] = event.data
            elif event.type == "output":
                outputs.append(str(event.data))

        if outputs:
            for output in outputs:
                print("\n" + output)
            return

        if not pending:
            raise RuntimeError(
                f"Workflow for {request.get('request_id')} ended without output "
                "or a manager approval request."
            )

        responses = {}
        for request_id, approval_request in pending.items():
            print("\n" + "=" * 70)
            print("MANAGER APPROVAL REQUIRED")
            print(approval_request.prompt)

            while True:
                answer = input().strip().lower()
                if answer in {"approve", "reject"}:
                    responses[request_id] = answer
                    break
                print("Invalid response. Please enter approve or reject: ", end="", flush=True)


async def run_local_simulation(records: list[dict[str, Any]]) -> None:
    """Produce Task 6 output without AI credentials, retaining human approval."""
    for original_request in records:
        request = dict(original_request)
        risk_level = assess_risk_level(request)
        business = evaluate_business_rules(request, risk_level=risk_level)
        request.update(business)

        if business["business_decision"] == "AUTO_APPROVE":
            decision = "AUTO_APPROVED"
        else:
            print("\n" + "=" * 70)
            print("MANAGER APPROVAL REQUIRED (local policy-only simulation)")
            print(f"Request ID: {request['request_id']}")
            print(f"Item: {request['product']}")
            print(f"Amount: INR {request['amount_inr']:,}")
            print(f"Eligibility issues: {', '.join(business['failed_checks'])}")
            print(
                f"Risk assessment: {risk_level} - "
                "Deterministic assessment of request amount, delivery age, "
                "invoice, condition/evidence, and return frequency."
            )
            while True:
                answer = input("Type approve or reject: ").strip().lower()
                if answer in {"approve", "reject"}:
                    break
                print("Invalid response. Please type approve or reject.")
            decision = (
                "MANAGER_APPROVED" if answer == "approve" else "MANAGER_REJECTED"
            )

        eligibility = "ELIGIBLE" if not business["failed_checks"] else "MANUAL_REVIEW"
        eligibility_explanation = (
            "All automatic-approval policy checks passed."
            if not business["failed_checks"]
            else "Automatic approval criteria were not all met; manager review was required."
        )
        if decision == "MANAGER_REJECTED":
            customer_message = (
                f"Your {request['request_type'].lower()} request for {request['product']} "
                "was reviewed and declined by a manager. This is a simulation; "
                "no refund or replacement has been processed."
            )
        else:
            customer_message = (
                f"Your {request['request_type'].lower()} request for {request['product']} "
                f"has been approved ({'automatically' if decision == 'AUTO_APPROVED' else 'by a manager'}) "
                "for the next processing step. This is a simulation; no actual refund "
                "or replacement has been initiated."
            )

        final_output = build_final_output(
            request=request,
            decision=decision,
            eligibility=eligibility,
            eligibility_explanation=eligibility_explanation,
            risk_level=risk_level,
            risk_summary=(
                "Deterministic assessment of request amount, delivery age, invoice, "
                "condition/evidence, and return frequency."
            ),
            customer_message=customer_message,
        )
        print("\n" + json.dumps(final_output, ensure_ascii=False, indent=2))


# Task 1 / Task 4: Load the input file and start a workflow for every return request.
async def run_with_agents() -> None:
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    base_url = os.getenv("AZURE_OPENAI_BASE_URL")
    model = os.getenv("AZURE_OPENAI_MODEL")

    if not all([api_key, base_url, model]):
        print(
            "Azure Foundry credentials are not configured. "
            "Running deterministic policy-only simulation."
        )
        records = load_return_requests(RETURNS_FILE)
        await run_local_simulation(records)
        return

    async with AsyncOpenAI(api_key=api_key, base_url=base_url) as client:
        chat_client = OpenAIChatClient(model=model, async_client=client)
        workflow = build_workflow(chat_client)

        records = load_return_requests(RETURNS_FILE)
        for request in records:
            print("\n" + "=" * 70)
            print(f"Processing {request['request_id']} | {request['product']}")
            await run_one(workflow, request)


if __name__ == "__main__":
    asyncio.run(run_with_agents())
