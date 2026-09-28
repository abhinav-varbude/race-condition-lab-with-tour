const vscode = require('vscode');

function workspaceRoot() {
  const folders = vscode.workspace.workspaceFolders;
  if (!folders || folders.length === 0) return null;
  return folders[0].uri;
}

async function openFile(relativePath) {
  const root = workspaceRoot();
  if (!root) {
    vscode.window.showErrorMessage('Open the lab folder first, then retry.');
    return;
  }
  const uri = vscode.Uri.joinPath(root, relativePath);
  const doc = await vscode.workspace.openTextDocument(uri);
  await vscode.window.showTextDocument(doc, { preview: false });
}

function runInTerminal(command) {
  let terminal = vscode.window.terminals.find(t => t.name === 'Lab');
  if (!terminal) {
    terminal = vscode.window.createTerminal('Lab');
  }
  terminal.show();
  terminal.sendText(command, true);
}

function activate(context) {
  // Auto-open the walkthrough the first time the extension starts in this codespace
  if (!context.globalState.get('raceLab.walkthroughShown')) {
    context.globalState.update('raceLab.walkthroughShown', true);
    setTimeout(() => vscode.commands.executeCommand('raceLab.openWalkthrough'), 2000);
  }

  context.subscriptions.push(
    vscode.commands.registerCommand('raceLab.openReadme', () => openFile('README.md')),
    vscode.commands.registerCommand('raceLab.openAccountFile', () => openFile('app/account.py')),
    vscode.commands.registerCommand('raceLab.runTests', () => runInTerminal('pytest tests/ -v')),
    vscode.commands.registerCommand('raceLab.runServer', () => runInTerminal('uvicorn app.main:app --reload')),
    vscode.commands.registerCommand('raceLab.openWalkthrough', () =>
      vscode.commands.executeCommand(
        'workbench.action.openWalkthrough',
        'race-condition-lab.race-condition-walkthrough#raceConditionLab',
        false
      )
    )
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
