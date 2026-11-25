The Healthcare Access Management aplication prototype I made was tested using the Ethereum Sepolia test network and dedicated test wallets. My testing focused on verifying the smart contract's permission management functions, invalid transaction handling and application integration. The prototype was tested on the Ethereum Sepolia test network rather than Ethereum mainnet. So, while the testing demonstrates the expected behaviour of the implemented functions but does not constitute a full independent security audit.

1. patient grants doctor access to record, the expected result was that the permission becomes valid, and the test passed
then patient checks granted permissions because the patient has access to check the permissions, the test passed
then doctor with access triest to revoke it but fails with a return prompt of "Access not currently granted", and the patient checked the permissions again, the doctor's attempt was rejected


