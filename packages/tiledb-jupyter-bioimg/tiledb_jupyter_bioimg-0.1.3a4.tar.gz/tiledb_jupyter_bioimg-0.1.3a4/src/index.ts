import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';
import { MODULE_NAME, MODULE_VERSION } from './version';
export * from './version';
import * as widgetExports from './widget';

/**
 * Initialization data for the @tiledb-inc/jupyter-bioimage-viewer extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: '@tiledb-inc/jupyter-bioimage-viewer',
  autoStart: true,
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension
};

export default extension;

/**
 * Activate the widget extension.
 */
function activateWidgetExtension(
  __: JupyterFrontEnd,
  registry: IJupyterWidgetRegistry
): void {
  registry.registerWidget({
    name: MODULE_NAME,
    version: MODULE_VERSION,
    exports: widgetExports
  });
}
