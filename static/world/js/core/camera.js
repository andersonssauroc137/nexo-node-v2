import { GAME_CONFIG } from "./config.js";


export class Camera {

    constructor() {

        this.x = 0;
        this.y = 0;
    }


    follow(
        target,
        world
    ) {

        const desiredX =
            target.x
            - GAME_CONFIG.canvas.width / 2;


        const desiredY =
            target.y
            - GAME_CONFIG.canvas.height / 2;


        const maxX =
            Math.max(
                0,
                world.width
                    - GAME_CONFIG.canvas.width
            );


        const maxY =
            Math.max(
                0,
                world.height
                    - GAME_CONFIG.canvas.height
            );


        this.x =
            Math.max(
                0,
                Math.min(
                    desiredX,
                    maxX
                )
            );


        this.y =
            Math.max(
                0,
                Math.min(
                    desiredY,
                    maxY
                )
            );
    }


    worldToScreen(
        x,
        y
    ) {

        return {
            x: x - this.x,
            y: y - this.y,
        };
    }
}