pragma solidity >=0.6.3;

// Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
// SPDX-License-Identifier:	AGPL-3.0-or-later

contract MinterTest {
	uint256 public totalMinted;
	uint256 public totalBurned;
	uint256 balance;
	
	event Burn(address indexed _burner, uint256 _burned);

	constructor(uint256 _mintValue) {
		totalMinted = _mintValue;
		balance = _mintValue;
	}

	function burn(address _from, uint256 _value, bytes calldata _data) public {
		_from;
		_data;
		burn(_value);
	}

	function burn(uint256 _value) public returns (bool) {
		burnCore(_value);
		return true;
	}

	function burnCore(uint256 _value) internal returns(uint256) {
		require(balance - _value >= 0);
		totalBurned += _value;
		balance -= _value;
		emit Burn(msg.sender, _value);
		return _value;
	}

	function burn() public returns (uint256) {
		return burnCore(totalMinted);
	}

	function supportsInterface(bytes4 _sum) public pure returns (bool) {
		if (_sum == 0x01ffc9a7) { // EIP165
			return true;
		}
		if (_sum == 0xbc4babdd) { // Burner
			return true;
		}
		return false;
	}
}
