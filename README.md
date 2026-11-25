# Healthcare Access Management – Decentralised Permission Management Application

## 1. Project Overview

For my project I created a decentralised healthcare information access management aplication prototype to demonstrate how blockchain technology can support patient's control over their electronic healthcare records. In my application, it allows a patient to grant or revoke a healthcare professional's access to a healthcare record identifier. The current permission status can also be checked through the application by anyone with access to it.
Based on my review paper research, my aim was to demonstrate how blockchain-based permission management can provide transparent, verifiable and tamper-resistant records of the permission changes.

## 2. Problem Statement

Traditional healthcare systems can involve separate organisations and centralised databases, making permission management and coordination challenging. So, my project explores whether blockchain technology can provide a transparent and verifiable method for managing permissions between patients and healthcare professionals.

## 3. Main Features

- Grant access to a healthcare professional
- Revoke previously granted access
- Check whether access is currently authorised
- Record permission changes through blockchain transactions

## 4. Technologies Used

- Solidity for smart contract development
- Remix IDE for smart contract compilation and deployment
- Ethereum Sepolia as the blockchain test network
- MetaMask for all wallet management
- Alchemy for blockchain RPC infrastructure
- Python via Google Colab for application code and development
- Web3.py for Python and blockchain integration
- Streamlit for my user interface
- GitHub as a source code management

## 5. System Architecture

My application prototype uses a Python Streamlit interface to communicate with a Solidity smart contract deployed on Ethereum Sepolia network. Then, Web3.py connects the Python application to the blockchain through an Alchemy RPC endpoint. The smart contract manages permission states using patient and healthcare professional wallet addresses and a fictional record identifier.

## 6. Smart Contract Functions

'grantAccess()' - grants a healthcare professional permission to access a specified record identifier
'revokeAccess()' - revokes previously granted permission
'checkAccess()' - checks the current permission status

The patient wallet address is used to identify the owner of each permission entry.

## 7. Privacy and Security

No real patient information, diagnoses or medical documents are stored on the blockchain, they still need to be stored in traditional databases, and oon-chain it's only the wallet addresses, record identifiers and permission statuses. Importantly, revoking permission changes the recorded permission state but cannot erase information that may already have been downloaded by the healtcare professional.

## 8. Testing

The smart contract and application were tested using Ethereum Sepolia and test wallets. My testing activities included granting access, revoking access, checking permission status, duplicate requests and invalid input scenarios.

## 9. Deployment

The smart contract was deployed to the Ethereum Sepolia test network.

Network: Ethereum Sepolia
Chain ID: 11155111
Blockchain infrastructure: Alchemy

## 10. Limitations and Future Improvements

This prototype does not host medical records or enforce access restrictions within external healthcare systems.
