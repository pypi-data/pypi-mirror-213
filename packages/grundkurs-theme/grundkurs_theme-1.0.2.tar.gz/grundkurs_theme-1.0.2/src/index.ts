import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ReadonlyPartialJSONObject } from '@lumino/coreutils';

import { CommandRegistry } from '@lumino/commands';

import { ICellFooter, Cell } from '@jupyterlab/cells';

import { CellFooterWithFeedback } from './widget';

import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';

import { IThemeManager } from '@jupyterlab/apputils';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IEditorServices } from '@jupyterlab/codeeditor';

import { requestAPI } from './handler';

const PLUGIN_ID = 'grundkurs_theme:plugin';

/**
 * Initialization data for the grundkurs_theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [INotebookTracker, IThemeManager, ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    tracker: INotebookTracker,
    manager: IThemeManager,
    settings: ISettingRegistry
  ) => {
    const { commands, shell } = app;
    const command = 'grundkurs:send-feedback';
    let url = '';

    /**
     * Load the settings for this extension
     *
     * @param setting Extension settings
     */
    function loadSetting(setting: ISettingRegistry.ISettings): void {
      // Read the settings and convert to the correct type
      url = setting.get('url').composite as string;
    }

    // Wait for the application to be restored and
    // for the settings for this plugin to be loaded
    Promise.all([app.restored, settings.load(PLUGIN_ID)]).then(
      ([, setting]) => {
        // Read the settings
        loadSetting(setting);

        // Listen for your plugin setting changes using Signal
        setting.changed.connect(loadSetting);

        commands.addCommand(command, {
          label: 'Send feedback for this assignment',
          execute: async args => {
            const current = getCurrent(tracker, shell, args);
            // We need a cellId therefore we need an activeCell
            if (current && current.content.activeCell) {
              const cellId = current.content.activeCell.model.id;
              const value = args['value'];
              // POST request
              const dataToSend = { cellId: cellId, url, value };
              try {
                console.log(JSON.stringify(dataToSend));
                const reply = await requestAPI<any>('feedback', {
                  body: JSON.stringify(dataToSend),
                  method: 'POST'
                });
                console.log(reply);
              } catch (reason) {
                console.error(
                  `Error on POST /feedback ${dataToSend}.\n${reason}`
                );
              }
            }
          }
        });
      }
    );

    console.log('JupyterLab extension grundkurs_theme is activated!');
    const style = 'grundkurs_theme/index.css';

    manager.register({
      name: 'grundkurs_theme',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

// Get the current widget and activate unless the args specify otherwise.
function getCurrent(
  tracker: INotebookTracker,
  shell: JupyterFrontEnd.IShell,
  args: ReadonlyPartialJSONObject
): NotebookPanel | null {
  const widget = tracker.currentWidget;
  const activate = args['activate'] !== false;

  if (activate && widget) {
    shell.activateById(widget.id);
  }

  return widget;
}

/**
 * Extend the default implementation of an `IContentFactory`.
 */
export class ContentFactoryWithFooterFeedback extends NotebookPanel.ContentFactory {
  constructor(
    commands: CommandRegistry,
    options: Cell.ContentFactory.IOptions
  ) {
    super(options);
    this.commands = commands;
  }
  /**
   * Create a new cell header for the parent widget.
   */
  createCellFooter(): ICellFooter {
    return new CellFooterWithFeedback(this.commands);
  }

  private readonly commands: CommandRegistry;
}

/**
 * The notebook cell factory provider.
 */
const cellFactory: JupyterFrontEndPlugin<NotebookPanel.IContentFactory> = {
  id: 'jupyterlab-cellcodebtn:factory',
  provides: NotebookPanel.IContentFactory,
  requires: [IEditorServices],
  autoStart: true,
  activate: (app: JupyterFrontEnd, editorServices: IEditorServices) => {
    // tslint:disable-next-line:no-console
    console.log(
      'JupyterLab extensionn grundkurs_theme',
      'overrides default nootbook content factory'
    );

    const { commands } = app;
    const editorFactory = editorServices.factoryService.newInlineEditor;
    return new ContentFactoryWithFooterFeedback(commands, { editorFactory });
  }
};

/**
 * Export these plugins as default.
 */
const plugins: Array<JupyterFrontEndPlugin<any>> = [plugin, cellFactory];

export default plugins;
