The Healthcare Access Management application prototype I made was tested using the Ethereum Sepolia test network and dedicated test wallets. My testing focused on verifying the smart contract's permission management functions, invalid transaction handling and application integration. The prototype was tested on the Ethereum Sepolia test network and Remix VM rather than Ethereum mainnet. So, while the testing demonstrates the expected behavior of the implemented functions but does not constitute a full independent security audit.

*Test 1* The patient grants doctor access to record, the expected result was that the permission becomes valid, and the test passed. Then patient checks granted permissions because the patient has access to check the permissions, the test passed.

*Test 2* Checking if the contract would grant access to zero address. The test passed as the request was invalid. 

*Test 3* The patients revokes the doctor's access to the record, and the access is indeed revoked, test passed.

*Test 4*  The doctor with access tries to revoke it but fails with a return prompt of "Access not currently granted", and the patient checked the permissions again, the doctor's attempt was rejected.

*Test 5* Doctor without access tries to grant it to themselves, the attempt is rejected, the test passed.


