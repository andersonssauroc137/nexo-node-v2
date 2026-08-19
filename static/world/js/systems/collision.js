export class CollisionSystem {

    static rectanglesOverlap(
        first,
        second
    ) {

        return (
            first.x
                < second.x
                + second.width

            &&

            first.x
                + first.width
                > second.x

            &&

            first.y
                < second.y
                + second.height

            &&

            first.y
                + first.height
                > second.y
        );
    }


    static collidesWithBuildings(
        collisionBox,
        buildings
    ) {

        return buildings.some(
            building =>

                this.rectanglesOverlap(
                    collisionBox,
                    building.collision
                )
        );
    }
}