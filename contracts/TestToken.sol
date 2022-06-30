// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./Lockable.sol";

contract TestToken is ERC20, Lockable {
    constructor() ERC20("Test Token", "TT") Lockable(address(this)) {}

    function mint(uint256 _amount) external {
        _mint(msg.sender, _amount);
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override(ERC20) {
        require(addressTokenLocked[from] != true);
        super._beforeTokenTransfer(from, to, amount);
    }
}
