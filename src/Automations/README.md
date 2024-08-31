
## Automator Integration

To enhance productivity, this project supports integration with macOS Automator, allowing users to automate text refinement tasks directly from their system with minimal effort. 

Quickly send selected text to the backend API for refinement and retrieve the improved version / review the diff in the app.

### Features of Automator Integration

- **Automated Text Refinement**: Quickly send selected text to the API and get the refined version back.
- **Single Shortcut Execution**: Set up a keyboard shortcut to streamline the process.
- **Visual Feedback**: Uses notifications and dialogs to provide feedback while the process runs.

### Setting Up Automator Workflow

1. **Open Automator**:
   - Go to `Applications` > `Automator` and create a new **Quick Action**.

2. **Configure the Quick Action**:
   - Set **"Workflow receives current"** to **"text"** in **"any application"**.
   - Choose **"Run Shell Script"** as the action to perform.

3. **Add the Shell Script**:
   - Copy and paste the shell scripts provided in this directory into the **Run Shell Script** action:

4. **Assign a Keyboard Shortcut**:
   - Open **System Settings** > **Keyboard** > **Keyboard Shortcuts** > **Services**.
   - Find your newly created Quick Action under the **Text** section and assign a shortcut to it.

5. **Run the Automator Workflow**:
   - Highlight any text in any application, and press the assigned keyboard shortcut to send the text to the API and retrieve the refined result.

### Example Usage with Automator

With this setup, you can easily refine text from anywhere on your Mac. Just select the text, use your assigned keyboard shortcut, and the refined text will be ready for use!
