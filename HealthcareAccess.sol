
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract HealthcareAccess {

    // Records whether a healthcare professional
    // has permission to access a patient's record.
    mapping(address => mapping(address => mapping(uint256 => bool)))
        private accessPermissions;

    // The patient grants access to a healthcare professional.
    function grantAccess(address doctor, uint256 recordId) public {
        require(doctor != address(0), "Invalid doctor address");
        require(doctor != msg.sender, "Cannot grant access to yourself");
        require(
            !accessPermissions[msg.sender][doctor][recordId],
            "Access already granted"
        );

        accessPermissions[msg.sender][doctor][recordId] = true;
    }

    // The patient revokes access.
    function revokeAccess(address doctor, uint256 recordId) public {
        require(doctor != address(0), "Invalid doctor address");
        require(
            accessPermissions[msg.sender][doctor][recordId],
            "Access not currently granted"
        );

        accessPermissions[msg.sender][doctor][recordId] = false;
    }

    // Anyone can check whether a doctor has permission
    // for a particular patient's record.
    function checkAccess(
        address patient,
        address doctor,
        uint256 recordId
    ) public view returns (bool) {
        return accessPermissions[patient][doctor][recordId];
    }
}
