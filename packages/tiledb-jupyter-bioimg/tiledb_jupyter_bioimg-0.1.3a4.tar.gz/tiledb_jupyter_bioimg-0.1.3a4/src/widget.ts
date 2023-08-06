// Copyright 2023 TileDB Inc.
// Licensed under the MIT License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers
} from '@jupyter-widgets/base';
import { MODULE_NAME, MODULE_VERSION } from './version';
import createViewer from '@tiledb-inc/bioimage-viewer';

export class BioImageViewerModel extends DOMWidgetModel {
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers
  };

  defaults(): any {
    return {
      ...super.defaults(),
      _model_name: BioImageViewerModel.model_name,
      _model_module: BioImageViewerModel.model_module,
      _model_module_version: BioImageViewerModel.model_module_version,
      _view_name: BioImageViewerModel.view_name,
      _view_module: BioImageViewerModel.view_module,
      _view_module_version: BioImageViewerModel.view_module_version
    };
  }

  static model_name = 'BioImageViewerModel';
  static view_name = 'BioImageViewerView';
}

interface IValues {
  basePath?: string;
  baseGroup?: string;
  token: string;
  groupID: string;
  namespace: string;
}

export class BioImageViewerView extends DOMWidgetView {
  values: IValues = this.model.get('value');

  render(): void {
    const wrapper = document.createElement('div');
    wrapper.style.height = '700px';
    this.el.appendChild(wrapper);

    createViewer({
      rootElement: wrapper,
      apiKey: this.values.token,
      groupID: this.values.groupID,
      basePath: this.values.basePath,
      baseGroup: this.values.baseGroup,
      namespace: this.values.namespace
    });
  }
}
