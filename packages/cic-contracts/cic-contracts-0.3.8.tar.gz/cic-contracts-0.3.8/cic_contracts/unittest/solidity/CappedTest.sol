pragma solidity >=0.6.3;

// Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
// SPDX-License-Identifier:	AGPL-3.0-or-later

contract CappedTest {
	event Cap(uint256 indexed _oldCap, uint256 _newCap);

	uint256 public maxSupply;

	constructor(uint256 _supply) {
		maxSupply = _supply;
	}

	function setMaxSupply(uint256 _supply) public {
		emit Cap(maxSupply, _supply);
		maxSupply = _supply;
	}

	function supportsInterface(bytes4 _sum) public pure returns (bool) {
		if (_sum == 0x01ffc9a7) { // EIP165
			return true;
		}
		if (_sum == 0x869f7594) { // Capped
			return true;
		}
		return false;
	}
}
