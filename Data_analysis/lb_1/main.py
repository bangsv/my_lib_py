import module

if __name__ == '__main__':
        try:
            name = str(input('Упражнение:\n(Вывод всех задач "?")\n'))
        except ValueError:
            print('Ошибка ввода')
        except KeyboardInterrupt:
            print('Выход')
        finally:
            if name == '?':
                module.help()    
            elif name == '1': 
                module.ex_1()
            elif name == '2':
                print("Res: ", module.ex_2(int(input('Введите число:'))))
            elif name == '3':
                module.ex_3()
            elif name == '4':
                print("Res: ", module.ex_4())
            elif name == '5':
                print("Res: ", module.ex_5())    
            elif name == '6':
                 module.ex_6()
            elif name == '7': 
                print("Res: ", module.ex_7())
            elif name == '8':
                module.ex_8()
            elif name == '9': 
                module.ex_9()
            elif name == '10':
                module.ex_10()
            elif name == '11':
                module.ex_11()