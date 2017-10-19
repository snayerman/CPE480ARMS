from PIL import Image
from deap import base, creator, tools
import sys
import os
import io
import random

NUM_GEN = 50
PROB_MATE = 0.5
PROB_MUT = 0.4

class ImageWrapper(object):
    def __init__(self, filename):
        img = Image.open(filename)
        bytesObj = io.BytesIO()

        img.save(self.data)
        img.close()

        self.bytes = bytearray(bytesObj.value())

        bytesObj.close()

    def __init__(self, img):
        self.bytes = bytearray(img.bytes)

def createImageInd(filename):
    img = creator.Image()   
    imgWrap = ImageWrapper(filename)
    img[:] = imgWrap.bytes

    return img

def combineImgs(img1, img2):
    tools.cxTwoPoint(img1.bytes, img2.bytes)

def mutateImg(img):
    mut = ImageWrapper(img)
    mut.bytes = tools.mutGaussian(img.bytes, 0, 1, 1, 1.0 / len(img.bytes))

    return mut

def evaluate(img):
    return sum(img.bytes)

def main():
    if len(sys.argv) < 2:
        print 'Usage: platform <img1> ...'
        sys.exit(1)

    creator.create('MaxFitness', base.Fitness, weights=(1.0,))
    creator.create('Image', bytearray, fitness=creator.MaxFitness)

    toolbox = base.Toolbox()
    toolbox.register('addImg', createImageInd)
    toolbox.register('mate', combineImgs)
    toolbox.register('mutate', mutateImg)
    toolbox.register('select', tools.selTournament, tournsize=3)
    toolbox.register('evaluate', evaluate)

    runIterations(toolbox)

def runIterations(toolbox):
    population = []
       
    for a in sys.argv[2:]:
        population.append(toolbox.createImageInd(a))

    for p in population:
        p.fitness.values = evaluate(p)

    for i in range(NUM_GEN):
        best = toolbox.select(population, len(population))
        best = [toolbox.clone(p) for p in best]

        for j in range(0, len(best), 2):
            img1 = best[i]

            if (i < len(best) - 1):
                img2 = best[i + 1]
                
                if random.random() < PROB_MATE:
                    toolbox.mate(img1, img2)
                    del img1.fitness.values
                    del img2.fitness.values

        for img in best:
            if random.random() < PROB_MUT:
                toolbox.mutate(img)
                del img.fitness.values

        for img in best:
            if not img.fitness.valid:
                img.fitness.values = toolbox.evaluate(img)

        population[:] = best

if __name__ == '__main__':
    main()
