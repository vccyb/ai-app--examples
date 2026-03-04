Title: Rewind file changes with checkpointing

URL Source: https://platform.claude.com/docs/en/agent-sdk/file-checkpointing

Markdown Content:
Guides

Track file changes during agent sessions and restore files to any previous state

File checkpointing tracks file modifications made through the Write, Edit, and NotebookEdit tools during an agent session, allowing you to rewind files to any previous state. Want to try it out? Jump to the [interactive example](https://platform.claude.com/docs/en/agent-sdk/file-checkpointing#try-it-out).

With checkpointing, you can:

*   **Undo unwanted changes** by restoring files to a known good state
*   **Explore alternatives** by restoring to a checkpoint and trying a different approach
*   **Recover from errors** when the agent makes incorrect modifications

Only changes made through the Write, Edit, and NotebookEdit tools are tracked. Changes made through Bash commands (like `echo > file.txt` or `sed -i`) are not captured by the checkpoint system.

How checkpointing works
-----------------------

When you enable file checkpointing, the SDK creates backups of files before modifying them through the Write, Edit, or NotebookEdit tools. User messages in the response stream include a checkpoint UUID that you can use as a restore point.

Checkpoint works with these built-in tools that the agent uses to modify files:

| Tool | Description |
| --- | --- |
| Write | Creates a new file or overwrites an existing file with new content |
| Edit | Makes targeted edits to specific parts of an existing file |
| NotebookEdit | Modifies cells in Jupyter notebooks (`.ipynb` files) |

File rewinding restores files on disk to a previous state. It does not rewind the conversation itself. The conversation history and context remain intact after calling `rewindFiles()` (TypeScript) or `rewind_files()` (Python).

The checkpoint system tracks:

*   Files created during the session
*   Files modified during the session
*   The original content of modified files

When you rewind to a checkpoint, created files are deleted and modified files are restored to their content at that point.

Implement checkpointing
-----------------------

To use file checkpointing, enable it in your options, capture checkpoint UUIDs from the response stream, then call `rewindFiles()` (TypeScript) or `rewind_files()` (Python) when you need to restore.

The following example shows the complete flow: enable checkpointing, capture the checkpoint UUID and session ID from the response stream, then resume the session later to rewind files. Each step is explained in detail below.

1.   Enable checkpointing Configure your SDK options to enable checkpointing and receive checkpoint UUIDs:

| Option | Python | TypeScript | Description |
| --- | --- | --- | --- |
| Enable checkpointing | `enable_file_checkpointing=True` | `enableFileCheckpointing: true` | Tracks file changes for rewinding |
| Receive checkpoint UUIDs | `extra_args={"replay-user-messages": None}` | `extraArgs: { 'replay-user-messages': null }` | Required to get user message UUIDs in the stream |  
2.   Capture checkpoint UUID and session ID With the `replay-user-messages` option set (shown above), each user message in the response stream has a UUID that serves as a checkpoint.

For most use cases, capture the first user message UUID (`message.uuid`); rewinding to it restores all files to their original state. To store multiple checkpoints and rewind to intermediate states, see [Multiple restore points](https://platform.claude.com/docs/en/agent-sdk/file-checkpointing#multiple-restore-points).

Capturing the session ID (`message.session_id`) is optional; you only need it if you want to rewind later, after the stream completes. If you're calling `rewindFiles()` immediately while still processing messages (as the example in [Checkpoint before risky operations](https://platform.claude.com/docs/en/agent-sdk/file-checkpointing#checkpoint-before-risky-operations) does), you can skip capturing the session ID. 
3.   Rewind files To rewind after the stream completes, resume the session with an empty prompt and call `rewind_files()` (Python) or `rewindFiles()` (TypeScript) with your checkpoint UUID. You can also rewind during the stream; see [Checkpoint before risky operations](https://platform.claude.com/docs/en/agent-sdk/file-checkpointing#checkpoint-before-risky-operations) for that pattern.

If you capture the session ID and checkpoint ID, you can also rewind from the CLI: 

Common patterns
---------------

These patterns show different ways to capture and use checkpoint UUIDs depending on your use case.

### Checkpoint before risky operations

This pattern keeps only the most recent checkpoint UUID, updating it before each agent turn. If something goes wrong during processing, you can immediately rewind to the last safe state and break out of the loop.

### Multiple restore points

If Claude makes changes across multiple turns, you might want to rewind to a specific point rather than all the way back. For example, if Claude refactors a file in turn one and adds tests in turn two, you might want to keep the refactor but undo the tests.

This pattern stores all checkpoint UUIDs in an array with metadata. After the session completes, you can rewind to any previous checkpoint:

Try it out
----------

This complete example creates a small utility file, has the agent add documentation comments, shows you the changes, then asks if you want to rewind.

Before you begin, make sure you have the [Claude Agent SDK installed](https://platform.claude.com/docs/en/agent-sdk/quickstart).

1.   Create a test file Create a new file called `utils.py` (Python) or `utils.ts` (TypeScript) and paste the following code: 
2.   Run the interactive example 

Create a new file called `try_checkpointing.py` (Python) or `try_checkpointing.ts` (TypeScript) in the same directory as your utility file, and paste the following code.

This script asks Claude to add doc comments to your utility file, then gives you the option to rewind and restore the original.

This example demonstrates the complete checkpointing workflow:

    1.   **Enable checkpointing**: configure the SDK with `enable_file_checkpointing=True` and `permission_mode="acceptEdits"` to auto-approve file edits
    2.   **Capture checkpoint data**: as the agent runs, store the first user message UUID (your restore point) and the session ID
    3.   **Prompt for rewind**: after the agent finishes, check your utility file to see the doc comments, then decide if you want to undo the changes
    4.   **Resume and rewind**: if yes, resume the session with an empty prompt and call `rewind_files()` to restore the original file

3.   Run the example Run the script from the same directory as your utility file.

Open your utility file (`utils.py` or `utils.ts`) in your IDE or editor before running the script. You'll see the file update in real-time as the agent adds doc comments, then revert back to the original when you choose to rewind. 
You'll see the agent add doc comments, then a prompt asking if you want to rewind. If you choose yes, the file is restored to its original state. 

Limitations
-----------

File checkpointing has the following limitations:

| Limitation | Description |
| --- | --- |
| Write/Edit/NotebookEdit tools only | Changes made through Bash commands are not tracked |
| Same session | Checkpoints are tied to the session that created them |
| File content only | Creating, moving, or deleting directories is not undone by rewinding |
| Local files | Remote or network files are not tracked |

Troubleshooting
---------------

### Checkpointing options not recognized

If `enableFileCheckpointing` or `rewindFiles()` isn't available, you may be on an older SDK version.

**Solution**: Update to the latest SDK version:

*   **Python**: `pip install --upgrade claude-agent-sdk`
*   **TypeScript**: `npm install @anthropic-ai/claude-agent-sdk@latest`

### User messages don't have UUIDs

If `message.uuid` is `undefined` or missing, you're not receiving checkpoint UUIDs.

**Cause**: The `replay-user-messages` option isn't set.

**Solution**: Add `extra_args={"replay-user-messages": None}` (Python) or `extraArgs: { 'replay-user-messages': null }` (TypeScript) to your options.

### "No file checkpoint found for message" error

This error occurs when the checkpoint data doesn't exist for the specified user message UUID.

**Common causes**:

*   File checkpointing was not enabled on the original session (`enable_file_checkpointing` or `enableFileCheckpointing` was not set to `true`)
*   The session wasn't properly completed before attempting to resume and rewind

**Solution**: Ensure `enable_file_checkpointing=True` (Python) or `enableFileCheckpointing: true` (TypeScript) was set on the original session, then use the pattern shown in the examples: capture the first user message UUID, complete the session fully, then resume with an empty prompt and call `rewindFiles()` once.

### "ProcessTransport is not ready for writing" error

This error occurs when you call `rewindFiles()` or `rewind_files()` after you've finished iterating through the response. The connection to the CLI process closes when the loop completes.

**Solution**: Resume the session with an empty prompt, then call rewind on the new query:

Next steps
----------

*   **[Sessions](https://platform.claude.com/docs/en/agent-sdk/sessions)**: learn how to resume sessions, which is required for rewinding after the stream completes. Covers session IDs, resuming conversations, and session forking.
*   **[Permissions](https://platform.claude.com/docs/en/agent-sdk/permissions)**: configure which tools Claude can use and how file modifications are approved. Useful if you want more control over when edits happen.
*   **[TypeScript SDK reference](https://platform.claude.com/docs/en/agent-sdk/typescript)**: complete API reference including all options for `query()` and the `rewindFiles()` method.
*   **[Python SDK reference](https://platform.claude.com/docs/en/agent-sdk/python)**: complete API reference including all options for `ClaudeAgentOptions` and the `rewind_files()` method.

Was this page helpful?
