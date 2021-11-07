from utils import *

import sys


# import tensorflow as tf


"""
input_1 = layers.Input((2, ))
input_2 = layers.Input((2, ))




inp1 = embedding_network(input_1)
inp2 = embedding_network(input_2)


merge_layer = layers.Lambda(p2_distance)([inp1, inp2])


output_layer = layers.Dense(1, activation="sigmoid")(merge_layer)


siamese = keras.Model(inputs=[input_1, input_2], outputs=output_layer)


siamese.compile(loss=loss(margin=1), optimizer="RMSprop", metrics=["accuracy"])



siamese.fit([np.array(dT[0]),np.array(dT[1])], np.array([1,1]).reshape(-1,1)
"""

def find_best_path(sxCoord: int, syCoord: int, radius: int, level: int):
    paths = getPathCoordinates(sxCoord, syCoord, radius)


    crashes = getTotalCrashes(paths)
    sinuodal = getSinuodalValue(paths)
    traffic = getTraffic(paths)
    fixedPaths = []
    for path in paths:
        fixedPaths.append([*map(lambda x: (x['lat'], x['lng']), path)])

    ed = compute_ed_from_acc(fixedPaths)

    maxScore = -float('inf')
    finalCoords = ()


    for path in range(len(paths)):
        score = 0
        if crashes[path] != 0:
            score+=(1/crashes[path])

        score+=1.5 * (1.008- sinuodal[path])

        score += 2 * (5-traffic[path])

        if level == 1:
            score*=8
            score-=ed[path]
        elif level == 2:
            score*=5
            score-=ed[path] * 2
        elif level == 3:
            score*=2
            score -= ed[path] * 4
        if score > maxScore:
            finalCoords = paths[path][-1]
            maxScore = score
    return finalCoords


lat = int(sys.argv[1])
lng = int(sys.argv[2])
radius = int(sys.argv[3])
level = int(sys.argv[4])


output = find_best_path(lat, lng, radius, level)


print(output['lat'], output['lng'])
        









