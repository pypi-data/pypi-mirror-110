// Copyright (c) Indresh Vishwakarma
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';
import { WorldModel } from './models/world_model';

import PQueue from 'p-queue';
const queue = new PQueue({ concurrency: 1 });

export class MazeModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: MazeModel.model_name,
      _model_module: MazeModel.model_module,
      _model_module_version: MazeModel.model_module_version,
      _view_name: MazeModel.view_name,
      _view_module: MazeModel.view_module,
      _view_module_version: MazeModel.view_module_version,
      current_call: '{}',
      method_return: '{}',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'MazeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'MazeView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class MazeView extends DOMWidgetView {
  world_model: WorldModel;

  method_changed = () => {
    let current_call: { method_name: string; params: any; cb: any } =
      JSON.parse(this.model.get('current_call'));

    if (current_call.method_name === 'halt') {
      return this.halt();
    } else {
      queue.add(() => {
        return new Promise((resolve) => {
          let ret =
            typeof this[current_call.method_name as keyof MazeView] ===
            'function'
              ? this[current_call.method_name as keyof MazeView].apply(
                  this,
                  current_call.params
                )
              : null;

          console.log('current_call in promise -> new code', current_call);
          let that = this;
          Promise.resolve(ret)
            .then(function (x) {
              // console.log("reached in promise");
              let data = JSON.stringify({
                value: x,
                cb: +new Date(),
                params: current_call.params,
                method: current_call.method_name,
              });
              console.log('setting return', data);
              that.model.set('method_return', data);
              that.model.save_changes();
              return data;
            })
            .then(resolve);
        });
      });
    }
  };

  draw_all = (
    rows: number,
    cols: number,
    vwalls: [],
    hwalls: [],
    robots = [],
    objects: any = {},
    tileMap: any = {},
    tiles: any = [],
    pending_goals: any = []
  ) => {
    return this.world_model.init(
      rows,
      cols,
      vwalls,
      hwalls,
      robots,
      objects,
      tileMap,
      tiles,
      pending_goals
    );
  };

  halt = () => {
    return queue.clear();
  };

  move_to = (index: number, x: number, y: number) => {
    return this.world_model.robots[index]?.move_to(x, y);
  };

  turn_left = (index: number) => {
    return this.world_model.robots[index]?.turn_left();
  };

  set_trace = (index: number, color: string) => {
    return this.world_model.robots[index]?.set_trace(color);
  };

  set_speed = (index: number, speed: number) => {
    return this.world_model.robots[index]?.set_speed(speed);
  };

  add_wall = (x: number, y: number, dir: string) => {
    return this.world_model.draw_wall(x, y, dir);
  };

  add_object = (x: number, y: number, obj_name: string, val: number) => {
    return this.world_model.draw_object(x, y, { [obj_name]: val });
  };

  update_object = (x: number, y: number, val: number) => {
    return this.world_model.update_object(x, y, val);
  };

  remove_object = (x: number, y: number) => {
    return this.world_model.remove_object(x, y);
  };

  remove_wall = (x: number, y: number, dir: string) => {
    return this.world_model.remove_wall(x, y, dir);
  };

  set_succes_msg = (msg: string[]) => {
    return this.world_model.success_msg(msg);
  };

  render() {
    //set methods
    this.method_changed();
    this.listenTo(this.model, 'change:current_call', this.method_changed);
    if (!this.world_model) {
      this.world_model = new WorldModel();
      this.el.appendChild(this.world_model.ui.wrapper);
    }
  }
}
