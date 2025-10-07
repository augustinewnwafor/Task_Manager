// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Decentralized To-Do List (Per-User Task Manager)
/// @notice Each user can create, complete, and delete ONLY their own tasks.
contract TodoList {
    // Task struct
    struct Task {
        uint id;
        string description;
        bool completed;
    }

    // user => (taskId => Task)
    mapping(address => mapping(uint => Task)) private tasks;

    // user => number of tasks created
    mapping(address => uint) private taskCount;

    // Events
    event TaskCreated(address indexed user, uint id, string description);
    event TaskCompleted(address indexed user, uint id, bool completed);
    event TaskDeleted(address indexed user, uint id);

    /// @notice Add a new task to your personal list
    function addTask(string memory _description) external {
        require(bytes(_description).length > 0, "Description required");

        taskCount[msg.sender]++;
        uint taskId = taskCount[msg.sender];

        tasks[msg.sender][taskId] = Task(taskId, _description, false);
        emit TaskCreated(msg.sender, taskId, _description);
    }

    /// @notice Mark a task as completed (or uncompleted)
    function toggleCompletion(uint _id) external {
        require(_id > 0 && _id <= taskCount[msg.sender], "Invalid task ID");
        Task storage task = tasks[msg.sender][_id];
        require(task.id != 0, "Task does not exist");

        task.completed = !task.completed;
        emit TaskCompleted(msg.sender, _id, task.completed);
    }

    /// @notice Delete a task from your list
    function deleteTask(uint _id) external {
        require(_id > 0 && _id <= taskCount[msg.sender], "Invalid task ID");
        require(tasks[msg.sender][_id].id != 0, "Task does not exist");

        delete tasks[msg.sender][_id];
        emit TaskDeleted(msg.sender, _id);
    }

    /// @notice Retrieve a specific task (only yours)
    function getTask(uint _id) external view returns (Task memory) {
        require(_id > 0 && _id <= taskCount[msg.sender], "Invalid task ID");
        require(tasks[msg.sender][_id].id != 0, "Task does not exist");

        return tasks[msg.sender][_id];
    }

    /// @notice Retrieve ALL your tasks in one call
    function getAllTasks() external view returns (Task[] memory) {
        uint count = taskCount[msg.sender];
        uint validCount = 0;

        // Count how many tasks exist (because some may be deleted)
        for (uint i = 1; i <= count; i++) {
            if (tasks[msg.sender][i].id != 0) {
                validCount++;
            }
        }

        // Create array with valid tasks only
        Task[] memory result = new Task[](validCount);
        uint index = 0;

        for (uint i = 1; i <= count; i++) {
            if (tasks[msg.sender][i].id != 0) {
                result[index] = tasks[msg.sender][i];
                index++;
            }
        }

        return result;
    }
}
