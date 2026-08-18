import { GAME_CONFIG } from "./config.js";


export class Camera {

    constructor() {
        this.x = 0;
        this.y = 0;
    }


    setPosition(x, y) {

        const maxX = Math.max(
            0,
            GAME_CONFIG.world.width
                - GAME_CONFIG.canvas.width
        );

        const maxY = Math.max(
            0,
            GAME_CONFIG.world.height
                - GAME_CONFIG.canvas.height
        );


        this.x = Math.max(
            0,
            Math.min(
                x,
                maxX
            )
        );

        this.y = Math.max(
            0,
            Math.min(
                y,
                maxY
            )
        );
    }


    worldToScreen(x, y) {

        return {
            x: x - this.x,
            y: y - this.y,
        };
    }
}