pragma solidity >=0.6.3;

// Author:	Louis Holbrook <dev@holbrook.no> 0826EDA1702D1E87C6E2875121D2E7BB88C2A746
// SPDX-License-Identifier:	AGPL-3.0-or-later

contract WriterTest {
	mapping (address => bool ) public isWriter;

	event WriterAdded(address _writer);
	event WriterDeleted(address _writer);

	function addWriter(address _writer) public returns (bool) {
		isWriter[_writer] = true;
		emit WriterAdded(_writer);
		return true;
	}

	function deleteWriter(address _writer) public returns (bool) {
		isWriter[_writer] = false;
		emit WriterDeleted(_writer);
		return true;
	}

	function supportsInterface(bytes4 _sum) public pure returns (bool) {
		if (_sum == 0x01ffc9a7) { // EIP165
			return true;
		}
		if (_sum == 0xabe1f1f5) { // Writer
			return true;
		}
		return false;
	}
}
