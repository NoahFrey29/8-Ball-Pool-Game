#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#include "phylib.h"

/*PART ONE*/
phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ) {

    phylib_object * newStillBall = malloc(sizeof(phylib_object)); // malloc

    if (newStillBall == NULL) { // in case of failure
	return NULL;
    }

    newStillBall->type = PHYLIB_STILL_BALL; // transfer over object type and set variable data

    newStillBall->obj.still_ball.number = number;
    newStillBall->obj.still_ball.pos.x = pos->x;
    newStillBall->obj.still_ball.pos.y = pos->y;

    return newStillBall;

}

phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ) {

    phylib_object * newRollingBall = malloc(sizeof(phylib_object)); // malloc

    if (newRollingBall == NULL) { // in case of failure
        return NULL;
    }

    newRollingBall->type = PHYLIB_ROLLING_BALL; // transfer over object type and set variable data
    newRollingBall->obj.rolling_ball.number = number;
    newRollingBall->obj.rolling_ball.pos.x = pos->x;
    newRollingBall->obj.rolling_ball.pos.y = pos->y;
    newRollingBall->obj.rolling_ball.vel.x = vel->x;
    newRollingBall->obj.rolling_ball.vel.y = vel->y;
    newRollingBall->obj.rolling_ball.acc.x = acc->x;
    newRollingBall->obj.rolling_ball.acc.y = acc->y;

    return newRollingBall;

}

phylib_object *phylib_new_hole( phylib_coord *pos ) {

    phylib_object * newHole = malloc(sizeof(phylib_object)); // malloc

    if (newHole == NULL) { // in case of failure
	return NULL;
    }

    newHole->type = PHYLIB_HOLE; // transfer over object type and set variable data
    newHole->obj.hole.pos.x = pos->x;
    newHole->obj.hole.pos.y = pos->y;

    return newHole;

}

phylib_object *phylib_new_hcushion(double y) {

    phylib_object * newHCushion = malloc(sizeof(phylib_object)); // malloc

    if(newHCushion == NULL) { // in case of failure
	return NULL;
    }

    newHCushion->type = PHYLIB_HCUSHION;
    newHCushion->obj.hcushion.y = y; // transfer over object type and set variable data

    return newHCushion;

}

phylib_object *phylib_new_vcushion(double x) {

    phylib_object * newVCushion = malloc(sizeof(phylib_object)); // malloc

    if(newVCushion == NULL) { // in case of failure
        return NULL;
    }

    newVCushion->type = PHYLIB_VCUSHION; // transfer over object type and set variable data
    newVCushion->obj.vcushion.x = x;

    return newVCushion;

}

phylib_table *phylib_new_table (void) {

    phylib_table * newTable = malloc(sizeof(phylib_table)); // malloc

    if(newTable == NULL) { // in case of failure
	return NULL;
    }

    newTable->time = 0.0; // set time

    newTable->object[0] = phylib_new_hcushion(0.0);
    newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    newTable->object[2] = phylib_new_vcushion(0.0);
    newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH); // call previous object constructors and add them to the table

    phylib_coord holeCoord1;
    phylib_coord holeCoord2;
    phylib_coord holeCoord3;
    phylib_coord holeCoord4;
    phylib_coord holeCoord5;
    phylib_coord holeCoord6;

    holeCoord1.x = 0;
    holeCoord1.y = 0;
    newTable->object[4] = phylib_new_hole(&holeCoord1); // 6 coords corresponding to 6 holes, added to the table too
    holeCoord2.x = PHYLIB_TABLE_WIDTH;
    holeCoord2.y = 0;
    newTable->object[5] = phylib_new_hole(&holeCoord2);

    holeCoord3.x = 0;
    holeCoord3.y = PHYLIB_TABLE_LENGTH/2;
    newTable->object[6] = phylib_new_hole(&holeCoord3);

    holeCoord4.x = PHYLIB_TABLE_WIDTH;
    holeCoord4.y = PHYLIB_TABLE_LENGTH/2;
    newTable->object[7] = phylib_new_hole(&holeCoord4);

    holeCoord5.x = 0;
    holeCoord5.y = PHYLIB_TABLE_LENGTH;
    newTable->object[8] = phylib_new_hole(&holeCoord5);

    holeCoord6.x = PHYLIB_TABLE_WIDTH;
    holeCoord6.y = PHYLIB_TABLE_LENGTH;
    newTable->object[9] = phylib_new_hole(&holeCoord6);

    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) { // setting other objects to NULL to ensure no uninitialized objects
	newTable->object[i] = NULL;
    }

    return newTable;

}

/*PART TWO*/
void phylib_copy_object( phylib_object **dest, phylib_object **src ) {


    if (src == NULL) { // check for null
	dest = NULL;
    }
    else {
        phylib_object * copy = malloc(sizeof(phylib_object)); // make space and assign to destination before memcopying
        *dest = copy;
        memcpy(*dest, *src, sizeof(phylib_object));
    }

}
phylib_table *phylib_copy_table( phylib_table *table ) {

    if (table == NULL) { // in case of NULL
	return table;
    }
    phylib_table * newTable = malloc(sizeof(phylib_table)); // make space

    if(newTable == NULL) { // in case of failure
        return NULL;
    }
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {

	newTable->object[i] = NULL; // set all values to NULL so they are not uninitialized
	if (table->object[i] != NULL) {
	    phylib_copy_object(&(newTable->object[i]), &(table->object[i])); // call copy object
	}
	else {
	    newTable->object[i] = NULL; // set to NULL
	}
    }
    newTable->time = table->time; // copy over table time

    return newTable;
}

void phylib_add_object( phylib_table *table, phylib_object *object ) {

    int check = 0;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
	if (table->object[i] == NULL && check == 0) { // loop to find an empty table spot
	    // assign object to NULL spot
	    table->object[i] = object;
	    check = 1; // exit
	}
    }
}
void phylib_free_table( phylib_table *table ) {

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
	if(table->object[i] != NULL) {
	    free(table->object[i]); // free everything non null
    	}
    }
    free(table); // free whole table
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ) {

    phylib_coord new_coord;
    new_coord.x = c1.x-c2.x; // subtract coords and return new coord
    new_coord.y = c1.y-c2.y;
    return new_coord;
}

double phylib_length( phylib_coord c ) {
    double xSq = c.x*c.x;
    double ySq = c.y*c.y;
    double length = 0;

    length = sqrt(xSq + ySq); // find the length of a coord and return it
    return length;

}

double phylib_dot_product( phylib_coord a, phylib_coord b ) {

    double x = a.x*b.x;  // find the dot product
    double y = a.y*b.y;
    double dot = x+y;
    return dot;

}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ) {

    double answer = 0.0;
    phylib_coord coord;
    if (obj1->type != PHYLIB_ROLLING_BALL) { // return -1 if obj1 isnt a rolling ball
	return -1.0;
    }

    if (obj2->type == PHYLIB_STILL_BALL) { // check each object type and complete its respective case
	coord = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
	answer = phylib_length(coord);
	answer = answer - (2*PHYLIB_BALL_RADIUS);
    }
    else if (obj2->type == PHYLIB_ROLLING_BALL) {
	coord = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
        answer = phylib_length(coord);
	answer = answer - (2*PHYLIB_BALL_RADIUS);
    }
    else if (obj2->type == PHYLIB_HOLE) {
	coord = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
        answer = phylib_length(coord);
        answer = answer - PHYLIB_HOLE_RADIUS;
    }
    else if (obj2->type == PHYLIB_HCUSHION) {
	answer = obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y;
	answer = fabs(answer) - PHYLIB_BALL_RADIUS;
    }
    else if (obj2->type == PHYLIB_VCUSHION) {
	answer = obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x;
	answer = fabs(answer) - PHYLIB_BALL_RADIUS;
    }
    else {
	return -1.0; // if not a valid object type return -1
    }
    return answer;
}


/*PART THREE*/
void phylib_roll( phylib_object *new, phylib_object *old, double time ) {

    double check = 0.0;
    if (new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) {
	// dont do anything
    }
    else { // complete position and velocity calculations for the new ball based on the old ball
	new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x*time) + (0.5*old->obj.rolling_ball.acc.x*(time*time));
	new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y*time) + (0.5*old->obj.rolling_ball.acc.y*(time*time));
	new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x*time);
	new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y*time);

        check = new->obj.rolling_ball.vel.x*old->obj.rolling_ball.vel.x; // check for sign change
	if (check < 0) {
	    new->obj.rolling_ball.vel.x = 0;
	    new->obj.rolling_ball.acc.x = 0;
	}
        // check both x and y velocities and if sign has changed, set to 0;
	check = new->obj.rolling_ball.vel.y*old->obj.rolling_ball.vel.y;
	if (check < 0) {
	    new->obj.rolling_ball.vel.y = 0;
	    new->obj.rolling_ball.acc.y = 0;
	}

    }

}

unsigned char phylib_stopped( phylib_object *object ) {

    unsigned char number = object->obj.rolling_ball.number;
    double x = object->obj.rolling_ball.pos.x;
    double y = object->obj.rolling_ball.pos.y;

    double length = phylib_length(object->obj.rolling_ball.vel); // find the length of velocity

    if (length < PHYLIB_VEL_EPSILON) { // turn into a still ball if less than epsilon
	object->type = PHYLIB_STILL_BALL;
	object->obj.still_ball.number = number;
	object->obj.still_ball.pos.x = x;
	object->obj.still_ball.pos.y = y;
	return 1; // return 1 flag
    }

    return 0; // else return 0 flag

}

void phylib_bounce( phylib_object **a, phylib_object **b ) {

    phylib_coord c;
    unsigned char number;

    phylib_coord r_ab;
    phylib_coord v_rel;
    phylib_coord n;
    double r_ab_length; // declare required variables
    double v_rel_n;
    double speedForA;
    double speedForB;

    switch((*b)->type) {
	case PHYLIB_HCUSHION: // cushion cases: change obj A's one dimensional velocities
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y*(-1);
	    (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.acc.y*(-1);
	    break;
	case PHYLIB_VCUSHION:
	    (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x*(-1);
            (*a)->obj.rolling_ball.acc.x = (*a)->obj.rolling_ball.acc.x*(-1);
	    break;
	case PHYLIB_HOLE: // free balls that fall into holes
	    free(*a);
	    *a = NULL;
	    break;
	case PHYLIB_STILL_BALL:
	    c = (*b)->obj.still_ball.pos;
	    number = (*b)->obj.still_ball.number;
	    (*b)->type = PHYLIB_ROLLING_BALL; // upgrade ball to rolling ball and transfer over still ball data
	    (*b)->obj.rolling_ball.pos = c;
	    (*b)->obj.rolling_ball.number = number;
	    (*b)->obj.rolling_ball.vel.x = 0;
            (*b)->obj.rolling_ball.vel.y = 0;
            (*b)->obj.rolling_ball.acc.x = 0;
            (*b)->obj.rolling_ball.acc.y = 0;
	    //get rid of this break to progress to the next case

	case PHYLIB_ROLLING_BALL:
	    r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos); // calculate relative positions and velocities
	    v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

	    r_ab_length = phylib_length(r_ab); // find normal vector
	    n.x = r_ab.x/r_ab_length;
	    n.y = r_ab.y/r_ab_length;

	    v_rel_n = phylib_dot_product(v_rel, n); // find dot product
	    (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x - (v_rel_n * n.x); // subtract from obj A
	    (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y - (v_rel_n * n.y);

	    (*b)->obj.rolling_ball.vel.x = (*b)->obj.rolling_ball.vel.x + (v_rel_n * n.x); // add to obj B
	    (*b)->obj.rolling_ball.vel.y = (*b)->obj.rolling_ball.vel.y + (v_rel_n * n.y);

	    speedForA = phylib_length((*a)->obj.rolling_ball.vel); // find the length of each speed
	    speedForB = phylib_length((*b)->obj.rolling_ball.vel);

	    if (speedForA > PHYLIB_VEL_EPSILON) { // if greater than epsilon, recalculate new acceleration for each object
		(*a)->obj.rolling_ball.acc.x = (-1)*((*a)->obj.rolling_ball.vel.x/speedForA * PHYLIB_DRAG);
		(*a)->obj.rolling_ball.acc.y = (-1)*((*a)->obj.rolling_ball.vel.y/speedForA * PHYLIB_DRAG);
	    }
	    if (speedForB > PHYLIB_VEL_EPSILON) {
                (*b)->obj.rolling_ball.acc.x = (-1)*((*b)->obj.rolling_ball.vel.x/speedForB * PHYLIB_DRAG);
                (*b)->obj.rolling_ball.acc.y = (-1)*((*b)->obj.rolling_ball.vel.y/speedForB * PHYLIB_DRAG);
            }
	    break;
    }

}

unsigned char phylib_rolling( phylib_table *t ) {
    unsigned char count = 0;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) { // loop through object list and check for rolling balls
	if (t->object[i] != NULL) {
            if (t->object[i]->type == PHYLIB_ROLLING_BALL) {
   	        count++;
	    }
	}
    }
    return count;
}

phylib_table *phylib_segment( phylib_table *table ) {

    phylib_table * newTable;
    double distance = 0.0;
    unsigned char stopped = 0;
    double time = PHYLIB_SIM_RATE;

    // find number of rolling balls
    unsigned char check = phylib_rolling(table);

    if (check == 0) { // return null when there is no more activity in the table
	return NULL;
    }
//    printf("after rolling check\n");
    // make a copt of the table
    newTable = phylib_copy_table(table); // think of the main table as the anchor and think of everything beyond that as a snap shot
//    printf("table copied\n");

    while (time < PHYLIB_MAX_TIME) { // loop over time
	//printf("in while, going for\n");
	for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) { // this for loop searches and rolls each rolling ball
	    //printf("in first for loop: i = %d\n", i);
	    if (newTable->object[i] == NULL) {
		// do nothing, prevent segmentation faults
	    }
	    else if (newTable->object[i]->type == PHYLIB_ROLLING_BALL) { // checks for rolling balls
		//printf("phylib roll is now rolling\n");
		phylib_roll(newTable->object[i], table->object[i], time); // call phylib roll with old table object and new copy table object
		//printf("%dth Object's pos: X: %f Y: %f\n", i+1,newTable->object[i]->obj.rolling_ball.pos.x, newTable->object[i]->obj.rolling_ball.pos.y);
	    }
	}
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) { // double for loop to calculate distances
	    for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
		//printf("in second for loop: j = %d\n", j);
	        if (i == j) {
		    //skip same objects to not get invalid distance calc
		}
		else if (newTable->object[j] == NULL) {
		    // doing nothing to skip seg faults
		}
		else {
		    if (newTable->object[i] == NULL){
			//do nothing - seg faults
		    }
		    else if (newTable->object[j] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL) { // check objects arent null and that i index is a rolling ball
			distance = phylib_distance(newTable->object[i], newTable->object[j]);
	                //printf("calcing distance = %f\n", distance);
	                if (distance <= 0) { // after calculating distance, check if it is less than or equal to 0
                            //printf("BOUNCING BOUNCING BOUNCING ***********************************\n");
                            phylib_bounce(&(newTable->object[i]), &(newTable->object[j]));
			    newTable->time = newTable->time + time; // call bounce and add the local time to the copied table time
                            return newTable; // return copied table
			}
		    }
		}
	    }
	}
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) { // for loop to check for stopped rolling balls
	    if (newTable->object[i] == NULL) {
                // do nothing, prevent segmentation faults
            }
            else if (newTable->object[i]->type == PHYLIB_ROLLING_BALL) {
                stopped = phylib_stopped(newTable->object[i]); // call phylib stopped with rolling balls
                if (stopped > 0) {
                    //printf("a ball has stopped\n");
                    newTable->time = newTable->time + time; // if stopped is flagged, add the local time to the copied table time
                    return newTable; // return copied table
                }
            }
        }
	time += PHYLIB_SIM_RATE; // increment time
//	printf("Time: %f\n", newTable->time);
    }
    newTable->time = newTable->time + time; // add the local time to the copied table time
    return newTable; // return copied table when max time is reached
}


/*NEW FUNCTION FOR A2*/
char *phylib_object_string( phylib_object *object ) {
    static char string[80];
    if (object==NULL)
    {
	sprintf( string, "NULL;" );
	return string;
    }

    switch (object->type)
    {
	case PHYLIB_STILL_BALL:
	    sprintf( string,
	    "STILL_BALL (%d,%6.1lf,%6.1lf)",
	    object->obj.still_ball.number,
	    object->obj.still_ball.pos.x,
	    object->obj.still_ball.pos.y );
	    break;
	case PHYLIB_ROLLING_BALL:
            sprintf( string,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;
	case PHYLIB_HOLE:
            sprintf( string,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
            break;
	case PHYLIB_HCUSHION:
            sprintf( string,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
            break;
	case PHYLIB_VCUSHION:
            sprintf( string,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
	    break;
    }
    return string;
}



