import {
    CollisionSystem
} from "./collision.js";


export class InteractionSystem {

    constructor() {

        this.activeInteraction =
            null;
    }


    update(
        player,
        buildings
    ) {

        const playerBox =
            player.getInteractionBox();


        this.activeInteraction =
            null;


        for (
            const building
            of buildings
        ) {

            if (
                !building
                    .interaction
                    .enabled
            ) {
                continue;
            }


            const isInside =
                CollisionSystem
                    .rectanglesOverlap(
                        playerBox,
                        building.interaction
                    );


            if (isInside) {

                this.activeInteraction = {
                    type:
                        building
                            .interaction
                            .type,

                    building,
                };

                break;
            }
        }
    }


    hasActiveInteraction() {

        return (
            this.activeInteraction
            !== null
        );
    }


    getActiveInteraction() {

        return (
            this.activeInteraction
        );
    }
}