import Konva from 'konva';
import { RobotModel } from './robot_model';
import $ from 'jquery';
import _isNumber from 'lodash/isNumber';
import _random from 'lodash/random';
import _padStart from 'lodash/padStart';

const walls_config: { [key: string]: any } = {
  normal: {
    x: 50,
    y: 25,
    stroke: 'darkred',
    strokeWidth: 10,
  },

  removable: {
    x: 50,
    y: 25,
    stroke: '#de1738',
    strokeWidth: 10,
  },

  goal: {
    x: 50,
    y: 25,
    stroke: 'darkred',
    strokeWidth: 7,
    dash: [5, 5],
  },
};

let MAX_WIDTH = 600;
let MAX_HEIGHT = 450;
let MAX_ROWS = 20;
let MAX_COLS = 20;
export class WorldModel {
  rows: number;
  cols: number;
  vwalls: any;
  hwalls: any;
  robots: any;
  width: number;
  height: number;
  bs: number;
  objects: any;
  tileMap: any;
  tiles: any;
  pending_goals: any;
  ui: {
    wrapper: HTMLDivElement;
    stage?: Konva.Stage;
    layers: {
      main: Konva.Layer;
      line: Konva.Layer;
      msg?: Konva.Layer;
      bg: Konva.Layer;
    };
  };

  constructor() {
    this.init_ui();
  }

  init(
    rows: number,
    cols: number,
    vwalls = [],
    hwalls = [],
    robots = [],
    objects = {},
    tileMap = {},
    tiles = [],
    pending_goals = []
  ) {
    this.rows = Math.min(MAX_ROWS, rows);
    this.cols = Math.min(MAX_COLS, cols);
    this.vwalls = vwalls;
    this.hwalls = hwalls;
    this.bs = Math.ceil(
      Math.min(MAX_HEIGHT / this.rows, MAX_WIDTH / this.cols, 50)
    );

    this.height = rows * this.bs;
    this.width = cols * this.bs;
    this.objects = objects;
    this.tileMap = tileMap;
    this.tiles = tiles;
    this.pending_goals = pending_goals;
    this.draw_canvas();

    this.robots = robots.map(
      (robot: RobotModel, i: number) =>
        new RobotModel(
          i,
          this,
          robot.x,
          robot.y,
          robot.orientation,
          robot.image
        )
    );

    console.log(robots);

    this.robots[0].draw();
  }

  init_ui() {
    let wrapper = document.createElement('div');
    wrapper.setAttribute('class', 'ttgt-wrapper');
    let elem = document.createElement('div');
    elem.setAttribute('id', 'container');

    let bttnTxt = document.createElement('span');
    let txtNode = document.createTextNode('Toggle');
    bttnTxt.appendChild(txtNode);
    bttnTxt.setAttribute('class', 'bttn-txt');

    let sidebar = document.createElement('button');
    sidebar.appendChild(bttnTxt);
    sidebar.setAttribute('class', 'ttgt-sidebar-bttn');
    sidebar.onclick = function () {
      $('#container').toggle();
    };

    wrapper.appendChild(elem);
    wrapper.appendChild(sidebar);

    this.ui = {
      wrapper,
      layers: {
        bg: new Konva.Layer({ offsetY: -150 }),
        main: new Konva.Layer({ offsetY: -150 }),
        line: new Konva.Layer({ offsetY: -150 }),
      },
    };
  }

  draw_canvas() {
    let padding = 25;
    let msgHeight = 150;
    let stage = new Konva.Stage({
      container: 'container',
      width: Math.max(this.width, 500) + this.bs + padding,
      height: this.height + this.bs + padding + msgHeight,
    });

    this.ui.layers.msg = new Konva.Layer({
      width: 500 + this.bs + padding,
      height: msgHeight,
    });

    stage.add(this.ui.layers.msg);
    stage.add(this.ui.layers.bg);
    stage.add(this.ui.layers.main);
    stage.add(this.ui.layers.line);
    this.ui.stage = stage;

    //draw stage
    this.draw_border();
    this.draw_grid();
    this.draw_objects();
    this.draw_msg_containers();

    if (this.pending_goals.length > 0) {
      this.draw_pending_instructions(this.pending_goals, 'red');
    } else {
      this.draw_pending_instructions(this.pending_goals);
    }

    this.ui.layers.main.draw();
  }

  draw_msg_containers() {
    let title = new Konva.Text({
      y: 10,
      width: 550,
      align: 'center',
      verticalAlign: 'center',
      height: 20,
      fontSize: 24,
      text: 'Pending Tasks',
    });

    this.ui.layers.msg?.add(title);
    this.ui.layers.msg?.draw();
  }

  draw_pending_instructions(
    msgs = ['No Goal'],
    color = 'black',
    fontSize = 16
  ) {
    let msg_layer = this.ui.layers.msg;

    let old_msg = this.ui.layers.msg?.find(`.instruction_msg`)[0];

    if (old_msg) {
      old_msg.destroy();
    }

    let msg = msgs.slice(0, 6).join('\n');
    let rect_width = Math.max(msg_layer?.width() || 0, 200) - 70;
    let text = new Konva.Text({
      padding: 10,
      text: msg,
      x: 40,
      y: 40,
      align: 'left',
      fill: color,
      lineHeight: 1.2,
      fontSize: fontSize,
      width: rect_width,
      name: 'instruction_msg-rect',
    });

    let rect = new Konva.Rect({
      width: rect_width,
      height: text.height(),
      cornerRadius: 10,
      stroke: 'black',
      x: 40,
      y: 40,
      name: 'instruction_msg',
    });
    msg_layer?.add(rect);
    msg_layer?.add(text);
    msg_layer?.draw();
  }

  success_msg(msg: string | string[]) {
    let arr: string[] = [];

    let old_msg = this.ui.layers.msg?.find(`.instruction_msg`)[0];
    let old_msg_rect = this.ui.layers.msg?.find(`.instruction_msg-rect`)[0];

    if (old_msg) {
      old_msg.destroy();
      old_msg_rect?.destroy();
    }
    return this.draw_pending_instructions(arr.concat(msg), 'green', 20);
  }

  draw_objects() {
    for (const key in this.objects) {
      const [x, y] = key.split(',').map((zz) => parseInt(zz));
      this.draw_object(x, y, this.objects[key]);
    }
  }

  draw_object(x: number, y: number, obj: any) {
    for (const obj_name in obj) {
      let val = this.parse_value(obj[obj_name]);

      if (obj_name === 'beeper') {
        this.draw_beeper(x, y, val);
      } else {
        this.draw_custom(obj_name, x, y, val);
      }
    }
  }

  update_object(x: number, y: number, val: number) {
    let text = this.ui.layers.main.find(`.obj-${x}-${y}-text`)[0];
    if (text) {
      //@ts-ignore
      text.text(`${val}`);
      this.ui.layers.main.draw();
    }
  }

  draw_beeper(x: number, y: number, val: number) {
    let radius = (0.6 * this.bs) / 2;
    let [cx, cy] = this.point2cxy(x + 1, y);
    cx = cx + this.bs / 2;
    let circle = new Konva.Circle({
      radius: radius,
      x: cx,
      y: cy,
      fill: 'yellow',
      stroke: 'orange',
      strokeWidth: 5,
      name: `obj-${x}-${y}-circle`,
    });

    let num = new Konva.Text({
      text: `${val}`,
      x: cx - 5,
      y: cy - 7,
      fontSize: 18,
      name: `obj-${x}-${y}-text`,
    });

    this.ui.layers.main.add(circle, num);
  }

  remove_object(x: number, y: number) {
    let circle = this.ui.layers.main.find(`.obj-${x}-${y}-circle`)[0];
    let text = this.ui.layers.main.find(`.obj-${x}-${y}-text`)[0];
    let img = this.ui.layers.main.find(`.obj-${x}-${y}-img`)[0];

    if (circle) {
      //@ts-ignore
      circle.destroy();
    }
    if (text) {
      //@ts-ignore
      text.destroy();
    }
    if (img) {
      //@ts-ignore
      img.destroy();
    }
    this.ui.layers.main.draw();
  }

  draw_custom(obj_name: string, x: number, y: number, val: number) {
    let imagePath = this.tileMap[obj_name];
    let [cx, cy] = this.point2cxy(x + 1, y);
    Konva.Image.fromURL(imagePath, (node: Konva.Image) => {
      node.setAttrs({
        x: cx + this.bs / 2 - 10,
        y: cy - this.bs / 2,
        width: this.bs - 10,
        height: this.bs - 10,
        name: `obj-${x}-${y}-img`,
      });
      this.ui.layers.main.add(node);
      this.ui.layers.main.batchDraw();
    });

    let num = new Konva.Text({
      text: `${val}`,
      x: cx + 32,
      y: cy + 2,
      fontSize: 16,
      name: `obj-${x}-${y}-text`,
    });
    this.ui.layers.main.add(num);
  }

  parse_value(val: number | string) {
    if (!val) return 0;
    if (_isNumber(val)) return val;
    else {
      const [min_val, max_val] = val.split('-').map((zz) => parseInt(zz));
      return _random(min_val, max_val);
    }
  }

  draw_border() {
    let box = new Konva.Rect({
      x: 50,
      y: this.bs / 2,
      stroke: 'darkred',
      strokeWidth: 10,
      closed: true,
      width: this.width,
      height: this.height,
    });

    this.ui.layers.main.add(box);
  }

  draw_grid() {
    this.draw_cols();
    this.draw_rows();
    this.draw_walls();
    this.draw_tiles();
  }

  _draw_tile(x: number, y: number, tile: string) {
    let [cx, cy] = this.point2cxy(x, y);
    let imagePath = this.tileMap[tile];
    Konva.Image.fromURL(imagePath, (node: Konva.Image) => {
      node.setAttrs({
        x: cx + 50,
        y: cy - this.bs / 2,
        width: this.bs,
        height: this.bs,
        name: `obj-${x}-${y}-tilebg`,
      });
      this.ui.layers.bg.add(node);
      this.ui.layers.bg.batchDraw();
    });
  }

  draw_tiles() {
    this.tiles.forEach((list: any, row: number) => {
      list.forEach((tile: any, col: number) => {
        if (!!tile) {
          this._draw_tile(row + 1, col + 1, tile);
        }
      });
    });
  }

  draw_cols() {
    for (let col = 1; col < this.cols; col++) {
      let line = new Konva.Line({
        x: 50,
        y: this.bs / 2,
        stroke: 'gray',
        points: [col * this.bs, 5, col * this.bs, this.height - 5],
      });

      let count = new Konva.Text({
        text: `${col}`,
        y: this.height + 40,
        x: col * this.bs + 25,
      });

      this.ui.layers.main.add(line, count);
    }

    let last_count = new Konva.Text({
      text: `${this.cols}`,
      y: this.height + 40,
      x: this.cols * this.bs + 25,
    });

    this.ui.layers.main.add(last_count);
  }

  draw_rows() {
    for (let row = 1; row < this.rows; row++) {
      let line = new Konva.Line({
        x: 50,
        y: this.bs / 2,
        stroke: 'gray',
        points: [this.width - 5, row * this.bs, 5, row * this.bs],
      });

      let count = new Konva.Text({
        text: `${this.rows + 1 - row}`,
        x: this.bs / 2,
        y: row * this.bs - 10,
      });

      this.ui.layers.main.add(line, count);
    }

    let last_count = new Konva.Text({
      text: `1`,
      x: 25,
      y: this.rows * this.bs - 10,
    });

    this.ui.layers.main.add(last_count);
  }

  point2cxy(x: number, y: number) {
    return [(x - 1) * this.bs, this.height - (y - 1) * this.bs];
  }

  draw_wall(x: number, y: number, dir: string, wall_type: string = 'normal') {
    let config = walls_config[wall_type];
    let border = null;
    let [cx, cy] = this.point2cxy(x, y);
    if (dir === 'east') {
      border = new Konva.Line({
        ...config,
        name: `vwall-${x}-${y}`,
        points: [cx + this.bs, cy - this.bs, cx + this.bs, cy],
      });
    }

    if (dir === 'north') {
      border = new Konva.Line({
        name: `hwall-${x}-${y}`,
        ...config,
        points: [cx, cy - this.bs, cx + this.bs, cy - this.bs],
      });
    }

    if (border) this.ui.layers.main.add(border);
  }

  remove_wall(x: number, y: number, dir: string) {
    if (dir !== 'north' && dir !== 'east') return;
    let wall = this.ui.layers.main.find(
      `.${dir === 'north' ? 'hwall' : 'vwall'}-${x}-${y}`
    )[0];
    if (wall) {
      wall.destroy();
    }
    this.ui.layers.main.draw();
  }

  draw_typed_wall(x: number, y: number, dir: string, val: number) {
    let [isGoal, isRemovable, isWall] = _padStart(
      Number(val).toString(2),
      3,
      '0'
    );

    if (parseInt(isWall)) {
      if (parseInt(isRemovable)) {
        this.draw_wall(x, y, dir, 'removable');
      } else {
        this.draw_wall(x, y, dir, 'normal');
      }
    } else if (parseInt(isGoal)) {
      this.draw_wall(x, y, dir, 'goal');
    }
  }

  draw_walls() {
    this.hwalls.forEach((hw: any, i: number) => {
      hw.forEach((val: number, j: number) => {
        if (val) {
          this.draw_typed_wall(i, j, 'north', val);
        } else {
          this.remove_wall(i, j, 'north');
        }
      });
    });

    this.vwalls.forEach((vw: any, i: number) => {
      vw.forEach((val: number, j: number) => {
        if (val) {
          this.draw_typed_wall(i, j, 'east', val);
        } else {
          this.remove_wall(i, j, 'east');
        }
      });
    });
  }
}
