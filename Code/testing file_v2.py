from SearchAlgorithm import *
from SubwayMap import *
from utils import *
from TestCases import *

def print_list_of_path_with_heu(path_list):
    for p in path_list:
        print("Route: {}, \t Cost: {}".format(p.route, round(p.h,2)))

if __name__=="__main__":
    ROOT_FOLDER = 'CityInformation/Lyon_SmallCity/'
    map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    map.add_connection(connections)

    infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
    map.add_velocity(infoVelocity_clean)



    ###BELOW HERE YOU CAN CALL ANY FUNCTION THAT YOU HAVE PROGRAMED TO ANSWER THE QUESTIONS FOR THE TEST###

    #Ejecutar tests aqui
    testing=TestCases()
    testing.setUp()
    # try:
    #     testing.test_Astar_improved()
    #     print("Test pasados con exito")
    # except Exception as e:
    #     print(e)
    
    testing.test_Astar_improved()
    # path1=Path([1,2,3])
    # path1.g=2
    # path2=Path([1,2,5])
    # path2.g=3
    # path3=Path([1,2,6])
    # path3.g=5
    # path4=Path([1,2,7])
    # path4.g=1
    
    # list1=[path1, path2]
    # list2=[path3, path4]
    
    # list3=insert_cost(list1, list2)
    # print_list_of_path_with_cost(list3)
    
    


