pragma solidity >=0.6.12;

// Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
// SPDX-License-Identifier:	AGPL-3.0-or-later

contract SealTest {
	event SealStateChange(bool indexed _final, uint256 _sealState);
	uint256 public sealState;
	uint256 public maxSealState = 7;

	function seal(uint256 _bits) public {
		require(sealState < maxSealState);
		sealState |= _bits;
	}

	function supportsInterface(bytes4 _sum) public pure returns (bool) {
		if (_sum == 0x01ffc9a7) { // EIP165
			return true;
		}
		if (_sum == 0x0d7491f8) { // Capped
			return true;
		}
		return false;
	}
}
