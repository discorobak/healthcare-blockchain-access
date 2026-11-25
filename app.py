
import os
import streamlit as st
from web3 import Web3
from eth_account import Account

# -----------------------------
# 1. Page setup
# -----------------------------

st.set_page_config(
    page_title="Healthcare Access Management",
    page_icon="💚",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #F4F8F7;
        color: #26332F;
    }

    h1 {
        color: #03594c !important;
    }

    h2, h3 {
        color: #168577 !important;
    }

    .stMarkdown, .stMarkdown p, label, li {
        color: #26332F !important;
    }

    .connection-status {
        color: #168577 !important;
        font-weight: 700;
    }

    [data-testid="stHeader"] {
        background-color: #F4F8F7;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #DCE8E5;
    }

    .stTextInput input, .stNumberInput input {
        background-color: white !important;
        color: #26332F !important;
        border: 1px solid #AABDB7;
        border-radius: 8px;
    }

    .stButton > button {
        background-color: #03594c !important;
        color: white !important;
        border: 1px solid #03594c;
        border-radius: 9px;
        font-weight: 600;
        min-height: 45px;
    }

    .stButton > button:hover {
        background-color: #047563 !important;
        color: white !important;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)
st.title("Healthcare Access Management")
st.write(
    "A decentralised application allowing patients "
    "to manage healthcare professional access to records."
)

# -----------------------------
# 2. Password protection
# -----------------------------

app_password = os.environ.get("APP_PASSWORD")

if not app_password:
    st.error("Application password is not configured.")
    st.stop()

if not st.session_state.get("authenticated", False):
    entered_password = st.text_input(
        "Enter application password",
        type="password"
    )

    if st.button("Log in"):
        if entered_password == app_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    st.stop()

# -----------------------------
# 3. Connect to blockchain
# -----------------------------

try:
    rpc_url = os.environ["ALCHEMY_RPC_URL"]
    private_key = os.environ["PATIENT_PRIVATE_KEY"]
    contract_address = Web3.to_checksum_address(
        os.environ["CONTRACT_ADDRESS"]
    )

    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_connected():
        st.error("Could not connect to Sepolia.")
        st.stop()

    if w3.eth.chain_id != 11155111:
        st.error("Connected network is not Sepolia.")
        st.stop()

    patient_account = Account.from_key(private_key)
    patient_address = Web3.to_checksum_address(
        patient_account.address
    )

except Exception:
    st.error("Blockchain configuration failed. Check your Colab setup.")
    st.stop()

# -----------------------------
# 4. Smart contract ABI
# -----------------------------

contract_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "doctor", "type": "address"},
            {"internalType": "uint256", "name": "recordId", "type": "uint256"}
        ],
        "name": "grantAccess",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "doctor", "type": "address"},
            {"internalType": "uint256", "name": "recordId", "type": "uint256"}
        ],
        "name": "revokeAccess",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "patient", "type": "address"},
            {"internalType": "address", "name": "doctor", "type": "address"},
            {"internalType": "uint256", "name": "recordId", "type": "uint256"}
        ],
        "name": "checkAccess",
        "outputs": [
            {"internalType": "bool", "name": "", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = w3.eth.contract(
    address=contract_address,
    abi=contract_abi
)

# -----------------------------
# 5. Display patient account
# -----------------------------

st.markdown(
    '<p class="connection-status">● Connected to Sepolia blockchain</p>',
    unsafe_allow_html=True
)

st.write("**Patient wallet:**")
st.code(patient_address)

st.divider()

# -----------------------------
# 6. User inputs
# -----------------------------

st.subheader("Manage Healthcare Record Access")

doctor_input = st.text_input(
    "Doctor's wallet address",
    placeholder="Enter doctor's public wallet address"
)

record_id = st.number_input(
    "Healthcare record ID",
    min_value=1,
    step=1
)

# -----------------------------
# 7. Validate doctor address
# -----------------------------

def get_doctor_address():
    try:
        doctor = Web3.to_checksum_address(doctor_input.strip())

        if doctor == "0x0000000000000000000000000000000000000000":
            st.error("The zero address is not valid.")
            return None

        if doctor == patient_address:
            st.error("You cannot grant access to yourself.")
            return None

        return doctor

    except Exception:
        st.error("Please enter a valid Ethereum wallet address.")
        return None

# -----------------------------
# 8. Send blockchain transaction
# -----------------------------

def send_permission_transaction(function_call):
    try:
        nonce = w3.eth.get_transaction_count(
            patient_address,
            "pending"
        )

        transaction = function_call.build_transaction({
            "from": patient_address,
            "nonce": nonce,
            "chainId": 11155111,
            "gasPrice": w3.eth.gas_price
        })

        gas_estimate = w3.eth.estimate_gas(transaction)
        transaction["gas"] = int(gas_estimate * 1.2)

        signed_transaction = patient_account.sign_transaction(
            transaction
        )

        tx_hash = w3.eth.send_raw_transaction(
            signed_transaction.raw_transaction
        )

        st.info("Transaction submitted. Waiting for confirmation...")

        receipt = w3.eth.wait_for_transaction_receipt(
            tx_hash,
            timeout=120
        )

        st.write("Transaction hash:")
        st.code(tx_hash.hex())

        if receipt.status == 1:
            st.success("Transaction confirmed on Sepolia!")
            st.write("Block number:", receipt.blockNumber)
        else:
            st.error("The blockchain transaction failed.")

    except Exception as error:
        st.error(
            "Transaction could not be completed. "
            "Check the permission status and wallet balance."
        )
        st.caption(str(error)[:500])

# -----------------------------
# 9. Grant and revoke buttons
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    if st.button("Grant Access", use_container_width=True):
        doctor = get_doctor_address()

        if doctor:
            send_permission_transaction(
                contract.functions.grantAccess(
                    doctor,
                    int(record_id)
                )
            )

with col2:
    if st.button("Revoke Access", use_container_width=True):
        doctor = get_doctor_address()

        if doctor:
            send_permission_transaction(
                contract.functions.revokeAccess(
                    doctor,
                    int(record_id)
                )
            )

# -----------------------------
# 10. Check permissions
# -----------------------------

st.divider()
st.subheader("Check Access Permission")

if st.button("Check Permission", use_container_width=True):
    doctor = get_doctor_address()

    if doctor:
        try:
            permission = contract.functions.checkAccess(
                patient_address,
                doctor,
                int(record_id)
            ).call()

            if permission:
                st.success("Doctor currently HAS access.")
            else:
                st.warning("Doctor currently DOES NOT have access.")

        except Exception:
            st.error("Unable to check permission.")

st.divider()

st.caption(
    "Educational prototype using fictional record IDs. "
    "No real patient information is stored."
)
