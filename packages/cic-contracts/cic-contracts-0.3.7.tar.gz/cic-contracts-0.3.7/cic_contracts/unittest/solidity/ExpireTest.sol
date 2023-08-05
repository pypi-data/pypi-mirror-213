pragma solidity >=0.6.3;

// Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
// SPDX-License-Identifier:	AGPL-3.0-or-later

contract ExpireTest {

	uint256 public expires;
	bool expired;

	event Expired(uint256 _timestamp);
	event ExpiryChange(uint256 indexed _oldTimestamp, uint256 _newTimestamp);

	constructor(uint256 _timestamp) {
		expires = _timestamp;
	}

	function setExpire(uint256 _timestamp) public {
		require(!expired);
		require(_timestamp > expires);
		emit ExpiryChange(expires, _timestamp);
		expires = _timestamp;
	}

	function applyExpiry() public returns(uint8) {
		if (expired) {
			return 1;
		}
		if (block.timestamp < expires) {
			return 0;
		}
		expired = true;
		emit Expired(block.timestamp);
		return 1;
	}

	function supportsInterface(bytes4 _sum) public pure returns (bool) {
		if (_sum == 0x01ffc9a7) { // EIP165
			return true;
		}
		if (_sum == 0x841a0e94) { // Expire
			return true;
		}
		return false;
	}
}

