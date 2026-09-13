import streamlit as st

from agent.disruption_detector import detect_disruptions
from agent.verifier import verify_inventory, verify_shipment
from agent.decision_agent import get_agent_decision

from tools.inventory import get_inventory
from tools.shipment import get_shipments
from tools.vendors import get_available_vendors
from tools.routes import get_available_routes
from tools.optimizer import rank_options

from tools.actions import (
    execute_purchase,
    execute_reroute
)

from simulation.disruptions import (
    simulate_shipment_delay,
    simulate_vendor_failure,
    simulate_stockout,
    simulate_route_closure
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Supply Chain Recovery Agent",
    page_icon="🚚",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🚚 Autonomous Retail Supply Chain Recovery Agent")

st.write(
    "AI-powered agent that monitors the supply chain, "
    "detects disruptions, evaluates recovery options, "
    "uses Gemini to make decisions and verifies recovery."
)


# ============================================================
# SESSION STATE
# ============================================================

if "recovery_plan" not in st.session_state:
    st.session_state.recovery_plan = None

if "recovery_disruption" not in st.session_state:
    st.session_state.recovery_disruption = None

if "ai_decision" not in st.session_state:
    st.session_state.ai_decision = None

if "agent_status" not in st.session_state:
    st.session_state.agent_status = "🟢 Monitoring"


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🚨 Disruption Simulator")

if st.sidebar.button("🚚 Simulate Shipment Delay"):

    simulate_shipment_delay("S001", 2)

    st.session_state.agent_status = "🔴 Shipment disruption detected"

    st.sidebar.success(
        "Shipment S001 delayed by 2 days!"
    )

    st.rerun()


if st.sidebar.button("🏪 Simulate Vendor Failure"):

    simulate_vendor_failure("V002")

    st.session_state.agent_status = "🔴 Vendor disruption detected"

    st.sidebar.success(
        "Vendor V002 is unavailable!"
    )

    st.rerun()


if st.sidebar.button("📦 Simulate Stockout"):

    simulate_stockout("P001")

    st.session_state.agent_status = "🔴 Inventory disruption detected"

    st.sidebar.success(
        "Gaming Laptop stock set to 0!"
    )

    st.rerun()


if st.sidebar.button("🛣️ Simulate Route Closure"):

    simulate_route_closure("R002")

    st.session_state.agent_status = "🔴 Route disruption detected"

    st.sidebar.success(
        "Route R002 has been closed!"
    )

    st.rerun()


# ============================================================
# LOAD DATA
# ============================================================

inventory = get_inventory()
shipments = get_shipments()


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

low_inventory_count = 0

for item in inventory:

    if item["stock"] < item["reorder_point"]:
        low_inventory_count += 1


delayed_shipments_count = 0

for shipment in shipments:

    if shipment["delay_days"] > 0:
        delayed_shipments_count += 1


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📦 Inventory Items",
        len(inventory)
    )

with col2:

    st.metric(
        "🚚 Shipments",
        len(shipments)
    )

with col3:

    st.metric(
        "⚠️ Active Problems",
        low_inventory_count + delayed_shipments_count
    )


# ============================================================
# AGENT STATUS
# ============================================================

st.subheader("🤖 Agent Status")

st.info(
    st.session_state.agent_status
)


# ============================================================
# INVENTORY
# ============================================================

st.header("📦 Inventory Status")

inventory_data = []


for item in inventory:

    if item["stock"] < item["reorder_point"]:

        status = "🔴 LOW"

    else:

        status = "🟢 OK"


    inventory_data.append({

        "Product": item["product"],

        "Warehouse": item["warehouse"],

        "Stock": item["stock"],

        "Reorder Point": item["reorder_point"],

        "Daily Demand": item["daily_demand"],

        "Status": status

    })


st.dataframe(
    inventory_data,
    use_container_width=True
)


# ============================================================
# SHIPMENTS
# ============================================================

st.header("🚛 Shipment Status")

shipment_data = []


for shipment in shipments:

    if shipment["delay_days"] > 0:

        status = "🔴 DELAYED"

    else:

        status = "🟢 ON TIME"


    shipment_data.append({

        "Shipment": shipment["shipment_id"],

        "Product": shipment["product"],

        "Origin": shipment["origin"],

        "Destination": shipment["destination"],

        "Status": status,

        "Delay": shipment["delay_days"],

        "Route": shipment.get(
            "route_id",
            "N/A"
        )

    })


st.dataframe(
    shipment_data,
    use_container_width=True
)


# ============================================================
# DISRUPTION DETECTION
# ============================================================

st.header("🔍 Disruption Detection")


disruptions = detect_disruptions(
    inventory,
    shipments
)


if disruptions:

    st.warning(
        f"⚠️ {len(disruptions)} disruption(s) detected!"
    )

    for disruption in disruptions:

        st.write(
            f"🔴 {disruption['message']}"
        )

else:

    st.success(
        "✅ No disruptions detected. "
        "Supply chain is operating normally."
    )


# ============================================================
# FUNCTION: CREATE PURCHASE OPTIONS
# ============================================================

def get_purchase_options(product_id):

    vendors = get_available_vendors(product_id)

    options = []

    # We want to purchase 20 units
    required_quantity = 20

    for vendor in vendors:

        # Ignore vendors that cannot provide
        # the required quantity

        if vendor["available_quantity"] >= required_quantity:

            options.append({

                "action": "PURCHASE",

                "vendor_id": vendor["vendor_id"],

                "vendor_name": vendor["name"],

                "cost": vendor["price"],

                "delivery_days": vendor["delivery_days"],

                "carbon": vendor["carbon"],

                "available_quantity":
                    vendor["available_quantity"]

            })


    return rank_options(options)


# ============================================================
# FUNCTION: CREATE ROUTE OPTIONS
# ============================================================

def get_route_options():

    routes = get_available_routes()

    options = []


    for route in routes:

        if route["available"]:

            options.append({

                "action": "REROUTE",

                "route_id": route["route_id"],

                "cost": route["cost"],

                "delivery_days": route["delivery_days"],

                "carbon": route["carbon"],

                "available": route["available"]

            })


    return rank_options(options)


# ============================================================
# AUTONOMOUS RECOVERY
# ============================================================

st.header("🤖 Autonomous Recovery")


# ============================================================
# RUN RECOVERY AGENT
# ============================================================

if st.button("🚀 Run Recovery Agent"):

    if not disruptions:

        st.info(
            "No disruption exists. "
            "Please simulate a disruption first."
        )

    else:

        # Take the most important disruption
        disruption = disruptions[0]

        st.session_state.recovery_disruption = disruption

        st.session_state.agent_status = (
            "🔍 Investigating disruption..."
        )


        # ====================================================
        # LOW INVENTORY
        # ====================================================

        if disruption["type"] == "LOW_INVENTORY":

            product_id = disruption["product_id"]

            st.write(
                "🔍 Investigating available vendors..."
            )

            options = get_purchase_options(
                product_id
            )


            if not options:

                st.error(
                    "❌ No feasible vendor found."
                )

                st.session_state.recovery_plan = None


            else:

                st.session_state.agent_status = (
                    "🧠 Gemini is analyzing vendors..."
                )

                st.subheader(
                    "📊 Available Recovery Options"
                )

                st.dataframe(
                    options,
                    use_container_width=True
                )


                # --------------------------------------------
                # GEMINI
                # --------------------------------------------

                decision = get_agent_decision(
                    disruption,
                    options
                )

                st.session_state.ai_decision = decision


                st.subheader(
                    "🧠 Gemini AI Decision"
                )

                st.json(decision)


                # --------------------------------------------
                # VALIDATE GEMINI DECISION
                # --------------------------------------------

                selected_vendor = None


                if decision.get("action") == "PURCHASE":

                    for option in options:

                        if (
                            option["vendor_id"]
                            == decision.get("vendor_id")
                        ):

                            selected_vendor = option

                            break


                if selected_vendor:

                    st.session_state.recovery_plan = (
                        selected_vendor
                    )

                    st.session_state.agent_status = (
                        "🟢 Valid recovery plan ready"
                    )

                    st.success(
                        "✅ Gemini selected a valid vendor."
                    )

                    st.info(
                        f"Recommended vendor: "
                        f"{selected_vendor['vendor_name']}"
                    )

                    st.write(
                        f"Confidence: "
                        f"{decision.get('confidence', 0) * 100:.0f}%"
                    )

                else:

                    st.error(
                        "❌ Gemini selected an invalid vendor."
                    )

                    st.session_state.recovery_plan = None


        # ====================================================
        # SHIPMENT DELAY
        # ====================================================

        elif disruption["type"] == "SHIPMENT_DELAY":

            st.write(
                "🔍 Investigating alternative routes..."
            )

            options = get_route_options()


            if not options:

                st.error(
                    "❌ No available route found."
                )

                st.session_state.recovery_plan = None


            else:

                st.session_state.agent_status = (
                    "🧠 Gemini is analyzing routes..."
                )

                st.subheader(
                    "🛣️ Available Recovery Routes"
                )

                st.dataframe(
                    options,
                    use_container_width=True
                )


                # --------------------------------------------
                # GEMINI
                # --------------------------------------------

                decision = get_agent_decision(
                    disruption,
                    options
                )

                st.session_state.ai_decision = decision


                st.subheader(
                    "🧠 Gemini AI Decision"
                )

                st.json(decision)


                # --------------------------------------------
                # VALIDATE DECISION
                # --------------------------------------------

                selected_route = None


                if decision.get("action") == "REROUTE":

                    for option in options:

                        if (
                            option["route_id"]
                            == decision.get("route_id")
                        ):

                            selected_route = option

                            break


                if selected_route:

                    st.session_state.recovery_plan = (
                        selected_route
                    )

                    st.session_state.agent_status = (
                        "🟢 Valid recovery plan ready"
                    )

                    st.success(
                        "✅ Gemini selected a valid route."
                    )

                    st.info(
                        f"Recommended route: "
                        f"{selected_route['route_id']}"
                    )

                    st.write(
                        f"Confidence: "
                        f"{decision.get('confidence', 0) * 100:.0f}%"
                    )

                else:

                    st.error(
                        "❌ Gemini selected an invalid route."
                    )

                    st.session_state.recovery_plan = None


# ============================================================
# SHOW SAVED RECOVERY PLAN
# ============================================================

if st.session_state.recovery_plan is not None:

    plan = st.session_state.recovery_plan

    disruption = st.session_state.recovery_disruption


    st.subheader("📋 Selected Recovery Plan")

    st.json(plan)


    # ========================================================
    # PURCHASE
    # ========================================================

    if plan["action"] == "PURCHASE":

        st.info(
            f"Vendor: {plan['vendor_name']}"
        )


        if st.button("💰 Execute Purchase"):

            st.session_state.agent_status = (
                "🚀 Executing purchase..."
            )

            result = execute_purchase(

                disruption["product_id"],

                20,

                plan["vendor_id"]

            )


            if result["status"] == "SUCCESS":

                st.success(
                    "✅ Purchase executed successfully!"
                )

                st.json(result)


                # --------------------------------------------
                # VERIFY
                # --------------------------------------------

                new_inventory = get_inventory()

                verification = verify_inventory(

                    new_inventory,

                    disruption["product_id"]

                )


                if verification["status"] == "SUCCESS":

                    st.session_state.agent_status = (
                        "🟢 Recovery verified successfully"
                    )

                    st.success(
                        "✅ Inventory recovery verified!"
                    )

                    st.write(
                        f"Current stock: "
                        f"{verification['stock']}"
                    )

                    # Clear old plan
                    st.session_state.recovery_plan = None

                    st.session_state.recovery_disruption = None

                else:

                    st.warning(
                        "⚠️ Inventory is still below "
                        "the required level."
                    )


            else:

                # =================================================
                # AUTOMATIC REPLANNING
                # =================================================

                st.error(
                    "❌ Purchase failed."
                )

                st.json(result)

                st.warning(
                    "🔄 Agent is automatically replanning..."
                )

                product_id = disruption["product_id"]

                new_options = get_purchase_options(
                    product_id
                )


                if new_options:

                    new_decision = get_agent_decision(
                        disruption,
                        new_options
                    )

                    st.subheader(
                        "🔄 New Gemini Decision"
                    )

                    st.json(new_decision)


                    new_plan = None


                    for option in new_options:

                        if (
                            option["vendor_id"]
                            == new_decision.get("vendor_id")
                            and new_decision.get("action")
                            == "PURCHASE"
                        ):

                            new_plan = option

                            break


                    if new_plan:

                        st.session_state.recovery_plan = (
                            new_plan
                        )

                        st.session_state.agent_status = (
                            "🔄 Replanned successfully"
                        )

                        st.success(
                            "✅ New recovery plan created!"
                        )

                    else:

                        st.error(
                            "❌ No valid alternative found."
                        )

                else:

                    st.error(
                        "❌ No alternative vendor available."
                    )


    # ========================================================
    # REROUTE
    # ========================================================

    elif plan["action"] == "REROUTE":

        st.info(
            f"Route: {plan['route_id']}"
        )


        if st.button("🚚 Execute Reroute"):

            st.session_state.agent_status = (
                "🚀 Executing reroute..."
            )

            result = execute_reroute(

                disruption["shipment_id"],

                plan["route_id"]

            )


            if result["status"] == "SUCCESS":

                st.success(
                    "✅ Shipment rerouted successfully!"
                )

                st.json(result)


                # --------------------------------------------
                # VERIFY
                # --------------------------------------------

                new_shipments = get_shipments()

                verification = verify_shipment(

                    new_shipments,

                    disruption["shipment_id"]

                )


                if verification["status"] == "SUCCESS":

                    st.session_state.agent_status = (
                        "🟢 Recovery verified successfully"
                    )

                    st.success(
                        "✅ Shipment recovery verified!"
                    )

                    # Clear old plan
                    st.session_state.recovery_plan = None

                    st.session_state.recovery_disruption = None

                else:

                    st.warning(
                        "⚠️ Shipment still needs recovery."
                    )


            else:

                # =================================================
                # AUTOMATIC REPLANNING
                # =================================================

                st.error(
                    "❌ Rerouting failed."
                )

                st.json(result)

                st.warning(
                    "🔄 Agent is automatically replanning..."
                )


                new_options = get_route_options()


                if new_options:

                    new_decision = get_agent_decision(

                        disruption,

                        new_options

                    )


                    st.subheader(
                        "🔄 New Gemini Decision"
                    )

                    st.json(
                        new_decision
                    )


                    new_plan = None


                    for option in new_options:

                        if (
                            option["route_id"]
                            == new_decision.get("route_id")
                            and new_decision.get("action")
                            == "REROUTE"
                        ):

                            new_plan = option

                            break


                    if new_plan:

                        st.session_state.recovery_plan = (
                            new_plan
                        )

                        st.session_state.agent_status = (
                            "🔄 Replanned successfully"
                        )

                        st.success(
                            "✅ New recovery plan created!"
                        )

                    else:

                        st.error(
                            "❌ No valid alternative route found."
                        )

                else:

                    st.error(
                        "❌ No alternative route available."
                    )



