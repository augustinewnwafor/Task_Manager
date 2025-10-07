# 🧠 Task Manager Smart Contract

A decentralized task management system built with **Solidity** and **Brownie**, deployed on the **Sepolia Testnet**.  
This contract lets users add, mark, and view tasks — all stored securely on the blockchain.

---

## 🚀 Features
- 📝 Add new tasks on-chain  
- ✅ Mark tasks as completed  
- 📜 View all tasks (transparent and immutable)  
- 🌐 Deployed on the Sepolia Ethereum test network  

---

## ⚙️ Tech Stack
- **Language:** Solidity (`^0.8.20`)
- **Framework:** Brownie
- **Network:** Sepolia Testnet
- **Wallet:** MetaMask
- **Provider:** Infura or Alchemy

---

## 🧩 Contract Example

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TaskManager {
    struct Task {
        string description;
        bool completed;
    }

    Task[] public tasks;

    function createTask(string memory _description) public {
        tasks.push(Task(_description, false));
    }

    function toggleTask(uint _index) public {
        require(_index < tasks.length, "Invalid index");
        tasks[_index].completed = !tasks[_index].completed;
    }

    function getTasks() public view returns (Task[] memory) {
        return tasks;
    }
}
