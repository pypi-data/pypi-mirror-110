import Konva from 'konva';
import { WorldModel } from './world_model';

const mod = (n: number, m: number) => {
  return ((n % m) + m) % m;
};

const _directions = [
  [0, 1],
  [-1, 0],
  [0, -1],
  [1, 0],
];

export const orientation_hash = {
  EAST: 0,
  NORTH: 1,
  WEST: 2,
  SOUTH: 3,
};

const rotation_diff = [
  { x: 10, y: 10 },
  { x: 10, y: 40 },
  { x: 40, y: 40 },
  { x: 40, y: 10 },
];

const robot_svg = `<svg xmlns="http://www.w3.org/2000/svg" version="1.1" class="svg-triangle" width='100' height='100' fill="#008080">
<path d="M 95,50 5,95 5,5 z"/>
</svg>`;

export class RobotModel {
  x: number;
  index: number;
  y: number;
  orientation: number;
  image?: string;
  canvas: Konva.Layer;
  node: Konva.Image | Konva.Path;
  points: any = [];
  traceColor: string = 'red';
  speed: number = 1;
  bs: number;

  world: WorldModel;

  constructor(
    index: number,
    world: WorldModel,
    x: number,
    y: number,
    orientation: number,
    image?: string
  ) {
    this.index = index;
    this.x = x;
    this.y = y;
    this.orientation = orientation;
    this.image = image;
    this.world = world;
    this.canvas = this.world.ui.layers.main;
    this.speed = 0.1;
    this.bs = this.world.bs;
  }

  cr2xy(x: number, y: number) {
    let [cx, cy] = this.world.point2cxy(x, y);
    let offset = rotation_diff[this.orientation];
    return [cx + 50 + offset.x, cy - 25 + offset.y];
  }

  trace_point(x: number, y: number) {
    let [cx, cy] = this.cr2xy(x, y);
    let [xr, yr] = _directions[mod(this.orientation - 1, 4)];
    console.log(xr, yr);
    let [xb, yb] = _directions[mod(this.orientation - 2, 4)];
    let offset = rotation_diff[this.orientation];
    return [cx + 5 * (xr + xb) - offset.x, cy - 5 * (yr + yb) - offset.y];
  }

  draw_trace() {
    let trace = new Konva.Line({
      points: this.points.slice(Math.max(this.points.length - 4, 0)),
      stroke: this.traceColor,
      x: this.bs / 2,
      y: this.bs / 2,
    });
    this.world.ui.layers.line.add(trace);
    this.world.ui.layers.line.draw();
  }

  add_point(x: number, y: number) {
    const [tx, ty] = this.trace_point(x, y);
    this.points = this.points.concat([tx, ty]);
    this.draw_trace();
  }

  set_trace(color: string) {
    this.traceColor = color;
    this.add_point(this.x, this.y);
  }

  set_speed(speed: number) {
    this.speed = speed;
  }

  clear_trace() {
    this.points = [];
    this.world.ui.layers.line.destroyChildren();
    this.world.ui.layers.line.draw();
  }

  move_to = (x: number, y: number) => {
    return new Promise((resolve) => {
      let [cx, cy] = this.cr2xy(x, y);
      let tween = new Konva.Tween({
        node: this.node,
        x: cx,
        y: cy,
        duration: this.speed,
        onFinish: () => {
          this.x = x;
          this.y = y;
          console.log('finished', x, y);
          this.add_point(x, y);
          resolve('done');
        },
      });

      tween.play();
    });
  };

  turn_left = () => {
    return new Promise((resolve) => {
      this.orientation = mod(this.orientation + 1, 4);
      let [cx, cy] = this.cr2xy(this.x, this.y);
      let tween = new Konva.Tween({
        node: this.node,
        rotation: mod(-90 * this.orientation, 360),
        duration: this.speed,
        x: cx,
        y: cy,
        onFinish: () => {
          this.node.rotation(mod(-90 * this.orientation, 360));
          this.add_point(this.x, this.y);
          console.log('finished', this.x, this.y);
          resolve('done');
        },
      });

      tween.play();
    });
  };

  draw() {
    let [cx, cy] = this.cr2xy(this.x, this.y);
    if (this.image) {
      Konva.Image.fromURL(this.image, (node: Konva.Image) => {
        node.setAttrs({
          x: cx,
          y: cy,
          width: this.bs - 15,
          height: this.bs - 15,
          rotation: -(this.orientation * 90),
        });
        this.node = node;
        this.canvas.add(this.node);
        this.canvas.batchDraw();
      });
    } else {
      let svg64 = btoa(robot_svg);
      var b64Start = 'data:image/svg+xml;base64,';
      var image64 = b64Start + svg64;

      Konva.Image.fromURL(image64, (node: Konva.Image) => {
        node.setAttrs({
          x: cx,
          y: cy,
          width: this.bs - 15,
          height: this.bs - 15,
          rotation: -(this.orientation * 90),
        });
        this.node = node;
        this.canvas.add(this.node);
        this.canvas.batchDraw();
      });
    }
  }
}
