import numpy as np
import pandas as pd
from scipy.stats import f as f_dist

def stepwise(df, ci):
    print("----------------------------------------------------------------------------")
    print(" _____    ______    _____    ______   ___   __   ___   __    _____    _____ ")
    print("|  ___|  |_    _|  |  ___|  |      |  \  \ |  | /  /  |  |  |  ___|  |  ___|")
    print("|  |__     |  |    | |___   |   ___|   \  \|  |/  /   |  |  |  |__   | |___ ")
    print(" __   |    |  |    | |___   |  |        \        /    |  |   __   |  | |___ ")
    print("|_____|    |__|    |_____|  |__|         \__/\__/     |__|  |_____|  |_____|")
    print("----------------------------------------------------------------------------")
    print("Stepwise Regression")
    start = str(input("Type 'Start' to run stepwise package:"))
    print("--------------------------------------------------")

    if start.lower() == 'start':
        # Run forward stepwise
        good_model = {}
        columns = list(df.columns[:-1])
        target = df.columns[-1]
        k = len(df.columns[[-1, 0]])

        while len(columns) > 0:
            forward_list_jkr = {}
            iterasi_forward = len(good_model) + 1

            jkr_list = []
            for column in columns:
                x = np.column_stack((np.ones(len(df)), np.array(df[column])))
                
                if len(good_model) > 0:
                    for key in good_model.keys():
                        x_additional = np.array(df[key])
                        x = np.column_stack((x, x_additional))
                
                g = np.dot(np.transpose(x), np.array(df[target]))
                b = np.dot(np.linalg.inv(np.dot(np.transpose(x), x)), g)
                jkr = (np.sum(np.dot(b, g)) - (sum(np.array(df[target]))**2/len(df)))
                jkr_list.append(jkr)
                jkr_now = jkr - sum(good_model.values())
                forward_list_jkr[column] = jkr_now

            print('forward stepwise')
            print()
            print(f"Iterasi ke-{iterasi_forward}")
            print()
            print("Jumlah Kuadrat Regresi")
            for key, value in forward_list_jkr.items():
                keys = list(good_model.keys())
                keys.append(key)
                if len(keys) > 1:
                    key_string = f"{'𝑅(𝛽_'}{key}{'|𝛽_'}{', '.join(keys[:-1])}{')'}"
                else:
                    key_string = f"{'𝑅(𝛽_'}{key}{')'}"
                print(f"{key_string}: {value}")
            
            print('Jumlah Kuadrat Total =', sum(np.array(df[target]) ** 2) - (sum(np.array(df[target])) ** 2 / len(df)))
            jkt = sum(np.array(df[target])**2) - (sum(np.array(df[target]))**2/len(df))
            max_jkr_column = max(forward_list_jkr, key=forward_list_jkr.get)
            s2 = (jkt - max(jkr_list)) / (len(df) - k)
            print('S2 =', s2)
            print(sum(good_model.values())+ forward_list_jkr[max_jkr_column])
            print('f_hitung =', forward_list_jkr[max_jkr_column] / s2)
            print('f_tabel =', f_dist.ppf(ci, 1, len(df) - k))
            check = (forward_list_jkr[max_jkr_column] / s2) > f_dist.ppf(ci, 1, len(df) - k)
            
            if check:
                # Add the significant predictor to the good_model
                print()
                print("atribut mempengaruhi model secara signifikan")
                good_model[max_jkr_column] = forward_list_jkr[max_jkr_column]
                print('model terbaik merupakan', list(good_model.keys()))
                print("--------------------------------------------------")
                columns.remove(max_jkr_column)
            else:
                print()
                print("--------------------------------------------------")
                print("atribut tidak mempengaruhi model secara signifikan")
                print("STOP!!!")
                print("--------------------------------------------------")
                break

            # Run backward stepwise
            if len(good_model) > 1:
                print("backward evaluation")
                print()
                backward_list_jkr = []
                print('cek dengan backward', list(good_model.keys())[:-1])

                #count jkr in best_model
                x = np.column_stack((np.ones(len(df)), np.array(df[list(good_model.keys())])))
                x1 = np.column_stack((np.ones(len(df)), np.array(df[list(good_model.keys())[-1]])))

                g = np.dot(np.transpose(x), np.array(df[target]))
                g1 = np.dot(np.transpose(x1), np.array(df[target]))
                b = np.dot(np.linalg.inv(np.dot(np.transpose(x), x)), g)
                b1 = np.dot(np.linalg.inv(np.dot(np.transpose(x1), x1)), g1)

                jkr_old = (np.sum(np.dot(b1, g1))) - (sum(np.array(df[target]))**2/len(df))
                backward_list_jkr.append(jkr_old)

                jkr = (np.sum(np.dot(b, g)) - (sum(np.array(df[target]))**2/len(df))) - sum(backward_list_jkr)

                keys = list(good_model.keys())
                print(f"{'𝑅(𝛽_'}{keys[0]}{'|𝛽_'}{','.join(keys[1:])}{')'} =", jkr)

                print('s2 =', s2)
                print('f_hitung =', jkr / s2)
                print('f_table =', f_dist.ppf(ci, 1, len(df) - k))
                print()
                check = (jkr / s2) < f_dist.ppf(ci, 1, len(df) - k)
                
                if check:
                    print('atribut tidak mempengaruhi model secara signifikan')
                    keys_to_delete = list(good_model.keys())[:-1]
                    new_model = {k: v for k, v in good_model.items() if k not in keys_to_delete}
                    good_model = new_model
                    print(good_model)

                else:
                    print('atribut mempengaruhi model secara signifikan')


                print("--------------------------------------------------")

            k+=1
            

        return list(good_model.keys())
    
    else:
        print("Your Input Is Wrong, Please Enter 'Start' Then Try Again!!!")
        print("--------------------------------------------------")
        return stepwise(df, ci)