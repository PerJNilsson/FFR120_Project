import numpy

#
# KNOWN MINOR BUGS : In GenerateNewCluster() periodic boundary conditions are not used when determining where
#                    to generate the next cluster. this is a minor bug thou which shouldn't have any effect
#                    for a large number of clusters
#

#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
class PlantCluster:
    numberOfPlantClusters=0
    numberOfClustersCreated=0 # Used to determine the unique ID value of each cluster.
    checkRadius=0


    def __init__(self,coordinates):
        self.x=coordinates[0]
        self.y=coordinates[1]
        self.ID=PlantCluster.numberOfClustersCreated # Every cluster has an unique ID used to link the
                                                     # plants to the cluster.
        PlantCluster.numberOfClustersCreated+=1
        PlantCluster.numberOfPlantClusters+=1

    def __del__(self):
        PlantCluster.numberOfPlantClusters-=1

    def GetCoordinates(self):
        return [self.x, self.y]

    def SetNumberOfPlantsInCluster(self,numberOfPlants):
        self.numberOfPlantsInCluster=numberOfPlants

    def setClusterCheckRadius(self,checkRadius):
        PlantCluster.checkRadius = checkRadius

    def getClusterCheckRadius(self):
        return PlantCluster.checkRadius

#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
class Plant:
    numberOfPlants=0    #
    plantObjects=[]     # Variables shared by all plant objects
    clusterObjects=[]   #
    maxNumberOfCharges = 23

    def __init__(self,coordinates,clusterID):
        self.x=coordinates[0]
        self.y=coordinates[1]
        self.clusterID=clusterID # This ID value links the plant to the correct cluster (its parent cluster).
        self.foodValue=40 # The amount of food recieved when consuming this plant.
        self.numberOfCharges = Plant.maxNumberOfCharges
        Plant.numberOfPlants += 1

    def __del__(self):
        Plant.numberOfPlants-=1

    def __str__(self):
        return "x = {}, y = {}".format(self.x, self.y)

    def UpdatePointers(self, plantObjects, clusterObjects):
        #
        # The function stores the references ("pointers") to the plant and cluster objects. Using these "pointers" one
        # can access all plant/cluster objects from any plant object.
        #
        Plant.plantObjects=plantObjects
        Plant.clusterObjects=clusterObjects

    def PlantGetsEaten(self):
        #
        # The function is called when a plant is eaten. It's assumed that the plant is destroyed when it's eaten (no charges).
        # The function also checks if the cluster should be destroyed aswell.
        #
        self.numberOfCharges -= 1 # one charge is used up
        if self.numberOfCharges == 0:
            for i in range(0, Plant.clusterObjects[0].numberOfPlantClusters,1): # Finds the cluster that the eaten plant belonged to
                if (Plant.clusterObjects[i].ID == self.clusterID):
                    Plant.clusterObjects[i].numberOfPlantsInCluster -= 1
                    if (Plant.clusterObjects[i].numberOfPlantsInCluster == 0): # If the plant destroyed was the last plant
                        Plant.clusterObjects.remove(Plant.clusterObjects[i])   # of the cluster the cluster will be destroyed
                    break
            Plant.plantObjects.remove(self) # Removes the eaten plant


#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
def PlantGrowth(clusterObjects, plantObjects, gridSize, spawnrate, distributionParameter,
                clusterSizeParameter,clusterStandardDeviation):
    #
    # The function checks if a new cluster should be formed, if so it calls on
    # another function which actually creates the new cluster.
    #

    r = numpy.random.rand()
    if (r<spawnrate):
        if(numpy.size(clusterObjects)==0):
            clusterObjects=[GenerateNewCluster(gridSize,clusterObjects,distributionParameter)]
            plantObjects=GenerateNewPlantsWithinCluster(clusterObjects[0],gridSize,clusterSizeParameter,clusterStandardDeviation)
        else:
            newClusterObject=GenerateNewCluster(gridSize,clusterObjects,distributionParameter)
            clusterObjects.append(newClusterObject)
            plantObjects.extend(GenerateNewPlantsWithinCluster(newClusterObject, gridSize, clusterSizeParameter,
                                                               clusterStandardDeviation))
    return clusterObjects, plantObjects


#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
def GenerateNewCluster(gridSize,clusterObjects,distributionParameter):
    #
    # This function creates the new cluster. The position of the new cluster may depend on the
    # positions of the current clusters or may be completely random, this depends on the
    # input parameter distributionParameter.
    #

    if(numpy.size(clusterObjects)==0 or distributionParameter==1):
        #
        # The coordinates are choosen randomly
        #
        coordinates=numpy.random.randint(0,gridSize,2)
        newCluster=PlantCluster(coordinates)
    else:
        #
        # The coordinates are choosen in such a way that there is a larger probability for the new
        # cluster to be formed far away from previous clusters.
        #
        numberOfClusters=clusterObjects[0].numberOfPlantClusters

        candidateCoordinates=numpy.random.randint(0,gridSize,(distributionParameter,2))
        distanceToClosestCluster=numpy.zeros((distributionParameter,1))

        for i in range(0,distributionParameter,1):
            # Loops over the candidate coordinates, in each loop the distance to the closest existing cluster is calculated.
            distanceToExistingClusters=numpy.zeros((numberOfClusters,1))
            currentCandidateCoordinates=candidateCoordinates[i,0::1]

            for j in range(0,numberOfClusters,1):
                # Loops over all existing clusters and calculates the distance from the clusters to the candidate coordinates.
                distanceToExistingClusters[j]=numpy.linalg.norm(currentCandidateCoordinates-clusterObjects[j].GetCoordinates())

            distanceToClosestCluster[i]=distanceToExistingClusters.min()# Distance to closest cluster for a given candidate.

        maxDistanceToClosestCluster=distanceToClosestCluster.max()
        for i in range(0,distributionParameter,1):
            # Loops over the candidates and selects the one with the largest distance to it's closest cluster
            # as the next cluster coordinates.
            if(distanceToClosestCluster[i]==maxDistanceToClosestCluster):
                newClusterCoordinates=candidateCoordinates[i]

        newCluster=PlantCluster(newClusterCoordinates)
    return newCluster


#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
def GenerateNewPlantsWithinCluster(clusterObject,gridSize,clusterSizeparameter,clusterStandardDeviation):
    #
    # The function creates the plant objects for the newly created cluster. The plant coordinates are taken from a
    # gaussian distribution with its mean in the centre of the newly generated cluster.
    #

    candidateXCoordinates = numpy.round(numpy.random.normal(clusterObject.x, clusterStandardDeviation, [clusterSizeparameter, 1]))
    candidateYCoordinates = numpy.round(numpy.random.normal(clusterObject.y, clusterStandardDeviation, [clusterSizeparameter, 1]))
    candidateCoordinates=numpy.hstack((candidateXCoordinates,candidateYCoordinates)) # Combines the x and y variables
                                                                                     # into one variable.
    uniqueCandidateCoordinates=numpy.unique(candidateCoordinates,axis=0) # Selects the unique coordinates (no duplicates)
    uniqueCandidateCoordinates=CheckBoundaryConditions(uniqueCandidateCoordinates,gridSize)
    newPlants=[Plant(coordinates, clusterObject.ID) for coordinates in uniqueCandidateCoordinates]

    clusterObject.SetNumberOfPlantsInCluster(numpy.size(newPlants))

    return newPlants


#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
def CheckBoundaryConditions(coordinates,gridSize):
    #
    # The function applies periodic boundary conditions. Used when new plants are generated.
    #
    coordinates[coordinates[0::1, 0] >= gridSize, 0] = coordinates[coordinates[0::1, 0] >= gridSize, 0] - gridSize # x
    coordinates[coordinates[0::1, 0] < 0, 0] = coordinates[coordinates[0::1, 0] < 0, 0] + gridSize               # x
    coordinates[coordinates[0::1, 1] >= gridSize, 1] = coordinates[coordinates[0::1, 1] >= gridSize, 1] - gridSize # y
    coordinates[coordinates[0::1, 1] < 0, 1] = coordinates[coordinates[0::1, 1] < 0, 1] + gridSize               # y
    return coordinates


#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
#=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=
def InitializePlants(numberOfClusters,gridSize, clusterDistributionParameter, clusterSizeParameter, clusterStandardDeviation):
    #
    # The function initializes the cluster and plant objects.
    #
    clusterObjects=[]
    plantObjects=[]
    for i in range(0,numberOfClusters,1):
        clusterObjects, plantObjects = PlantGrowth(clusterObjects, plantObjects, gridSize,1,clusterDistributionParameter,
                                                            clusterSizeParameter,clusterStandardDeviation)
        plantObjects[0].UpdatePointers(plantObjects, clusterObjects)
    return clusterObjects, plantObjects




