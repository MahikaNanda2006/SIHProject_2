// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SupplyChain {

    struct CollectionEvent {
        string collectorName;
        string location;
        uint timestamp;
    }

    struct ProvenanceEvent {
        string ownerName;
        string location;
        uint timestamp;
    }

    struct Item {
        string itemId;
        CollectionEvent collection;
        ProvenanceEvent[] provenanceHistory;
    }

    mapping(string => Item) private items;

    // Add a collection event for a new item
    function addCollectionEvent(string memory itemId, string memory collectorName, string memory location) public {
        require(bytes(items[itemId].itemId).length == 0, "Item already exists");
        CollectionEvent memory cEvent = CollectionEvent(collectorName, location, block.timestamp);
        items[itemId].itemId = itemId;
        items[itemId].collection = cEvent;
    }

    // Add a provenance event for an existing item
    function addProvenanceEvent(string memory itemId, string memory ownerName, string memory location) public {
        require(bytes(items[itemId].itemId).length != 0, "Item does not exist");
        ProvenanceEvent memory pEvent = ProvenanceEvent(ownerName, location, block.timestamp);
        items[itemId].provenanceHistory.push(pEvent);
    }

// Return basic item info
function getItemBasic(string memory itemId) public view returns (string memory, string memory, string memory, uint) {
    require(bytes(items[itemId].itemId).length != 0, "Item does not exist");
    Item storage item = items[itemId];
    return (
        item.itemId,
        item.collection.collectorName,
        item.collection.location,
        item.collection.timestamp
    );
}

// Return number of provenance events
function getProvenanceCount(string memory itemId) public view returns (uint) {
    require(bytes(items[itemId].itemId).length != 0, "Item does not exist");
    return items[itemId].provenanceHistory.length;
}

// Return a single provenance event by index
function getProvenanceEvent(string memory itemId, uint index) public view returns (string memory, string memory, uint) {
    require(bytes(items[itemId].itemId).length != 0, "Item does not exist");
    ProvenanceEvent storage pEvent = items[itemId].provenanceHistory[index];
    return (pEvent.ownerName, pEvent.location, pEvent.timestamp);
}


    // Get provenance history as separate arrays
    function getProvenanceHistory(string memory itemId) public view returns (string[] memory, string[] memory, uint[] memory) {
        require(bytes(items[itemId].itemId).length != 0, "Item does not exist");
        Item storage item = items[itemId];
        uint len = item.provenanceHistory.length;

        string[] memory ownerNames = new string[](len);
        string[] memory locations = new string[](len);
        uint[] memory timestamps = new uint[](len);

        for (uint i = 0; i < len; i++) {
            ProvenanceEvent storage p = item.provenanceHistory[i];
            ownerNames[i] = p.ownerName;
            locations[i] = p.location;
            timestamps[i] = p.timestamp;
        }

        return (ownerNames, locations, timestamps);
    }
}
