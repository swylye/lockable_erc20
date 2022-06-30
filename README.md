# lockable_erc20

Lockable.sol builds upon existing functionalities of ERC20 and allows tokens to be locked to specific controller address. Only controller address can initiate unlock.

Depending on how you'd like to use the locking mechanism, you can add additional require parameters before certain functions can be initiated.

In this example, locked tokens cannot be transferred.
