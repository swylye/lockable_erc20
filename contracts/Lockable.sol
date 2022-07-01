// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Lockable {
    IERC20 tokenContract;

    mapping(address => bool) public addressTokenLocked;
    mapping(address => address) public addressTokenController;

    constructor(address _tokenAddress) {
        tokenContract = IERC20(_tokenAddress);
    }

    function lockToken(address _controller, bool _proxy) public {
        address tokenOwner;
        if (_proxy) {
            tokenOwner = tx.origin;
        } else {
            tokenOwner = msg.sender;
        }
        require(
            addressTokenLocked[tokenOwner] != true,
            "Token is already locked!"
        );
        require(
            tokenContract.balanceOf(tokenOwner) > 0,
            "You must own token(s) in order to lock!"
        );
        require(_controller != address(0), "Controller address must not be 0!");
        addressTokenLocked[tokenOwner] = true;
        addressTokenController[tokenOwner] = _controller;
    }

    function unlockToken(address _tokenOwner) public {
        require(
            addressTokenLocked[_tokenOwner] == true,
            "Token is not locked!"
        );
        require(
            msg.sender == addressTokenController[_tokenOwner],
            "Only designated controller address can initiate unlock!"
        );
        addressTokenLocked[_tokenOwner] = false;
        delete addressTokenController[_tokenOwner];
    }
}
