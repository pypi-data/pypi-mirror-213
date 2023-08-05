pragma solidity >=0.6.3;

// Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
// SPDX-License-Identifier:	AGPL-3.0-or-later

contract MinterTest {
	mapping (address => uint256) public balance;
		
	event Mint(address indexed _minter, address indexed _beneficiary, uint256 _value);

	function mintTo(address _beneficiary, uint256 _value) public returns (bool) {
		balance[_beneficiary] += _value;	
		emit Mint(msg.sender, _beneficiary, _value);
		return true;
	}

	function mint(address _beneficiary, uint256 _value, bytes calldata _data) public {
		_data;
		mintTo(_beneficiary, _value);
	}
	function safeMint(address _beneficiary, uint256 _value, bytes calldata _data) public {
		_data;
		mintTo(_beneficiary, _value);
	}

	function supportsInterface(bytes4 _sum) public pure returns (bool) {
		if (_sum == 0x01ffc9a7) { // EIP165
			return true;
		}
		if (_sum == 0x5878bcf4) { // Minter
			return true;
		}
		return false;
	}
}
