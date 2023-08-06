import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the jupyterlab_theme_minimalist extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_theme_minimalist',
  requires: [IThemeManager],
  autoStart: true,
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension jupyterlab_theme_minimalist is activated!');
    const style = 'jupyterlab_theme_minimalist/index.css';

    manager.register({
      name: 'jupyterlab_theme_minimalist',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default extension;
