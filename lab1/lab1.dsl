workspace "Бюждетирование" {
    model {
        user = person "Пользователь" {
            description "Пользователь, который управляет своими доходами и расходами"
        }
        
        budgetingApp = softwareSystem "Система бюджетирования" {
            description "Система для учета доходов, расходов и анализа бюджета"
            
            userActions = container "Взаимодействия с пользователями"  {
                description "Обрабатывает регистрацию и поиск пользователей"
                technology "FastAPI"
      
                createUser = component "Создание нового пользователя" {
                    description "Обрабатывает регистрацию пользователей"
                    technology "Spring Web"
                }
                
                searchUserLogin = component "Поиск пользователя по логину" {
                    description "Ищет пользователя по логину"
                    technology "Spring Web"
                }
                
                searchUserMask = component "Поиск пользователя по маске имя и фамилии" {
                    description "Ищет пользователей по имени и фамилии"
                    technology "Spring Web"
                }
            }
                
            budgetingActions = container "Управление бюджетом" {
                description "Обрабатывает доходы и расходы пользователей"
                technology "FastAPI" 
                
                createIncome = component "Создание планируемого дохода" {
                    description "Добавляет новый планируемый доход"
                    technology "Spring Web"
                }
                
                listIncome = component "Получение перечня доходов" {
                    description "Выдает список всех планируемых доходов"
                    technology "Spring Web"
                }
                
                createExpense = component "Создание планируемого расхода" {
                    description "Добавляет новый планируемый расход"
                    technology "Spring Web"
                }

                listExpense = component "Получение перечня расходов" {
                    description "Выдает список всех планируемых расходов"
                    technology "Spring Web"
                }
                
                budgetDynamics = component "Расчет динамики бюджета" {
                    description "Анализирует изменения бюджета за период"
                    technology "Spring Web"
                }
            }
            
            dbUsers = container "База данных пользователей" {
                technology "PostgreSQL"
                description "Хранит информацию о пользователях"
            }

            dbBudget = container "База данных бюджета" {
                technology "PostgreSQL"
                description "Хранит информацию о доходах и расходах пользователей"
            }
        }
        
        //Взаимодействия    
        user -> createUser "Создание пользователя"
        createUser -> dbUsers "Записывает данные о пользователях"

        user -> searchUserLogin "Поиск пользователя по логину"
        dbUsers -> searchUserLogin "Читает данные о пользователях по логину"

        user -> searchUserMask "Поиск пользователя имени"
        dbUsers -> searchUserMask "Читает данные о пользователях по имени"

        user -> createIncome "Добавление дохода"
        createIncome -> dbBudget "Сохраняет данные о доходах"

        user -> listIncome "Получение списка доходов"
        dbBudget -> listIncome "Читает данные о доходах"

        user -> createExpense "Добавление расхода"
        createExpense -> dbBudget "Сохраняет данные о расходах"

        user -> listExpense "Получение списка расходов"
        dbBudget -> listExpense "Читает данные о расходах"

        user -> budgetDynamics "Расчет динамики бюджета"
        budgetDynamics -> dbBudget "Анализирует данные о доходах и расходах"
    }
    
    views {
        themes default

        dynamic userActions "UserOperations" {
        user -> createUser "Регистрация пользователя"
        user -> searchUserLogin "Поиск по логину"
        user -> searchUserMask "Поиск по имени"
        autoLayout
        }

        dynamic budgetingActions "BudgetOperations" {
            user -> createIncome "Добавление дохода"
            user -> createExpense "Добавление расхода"
            user -> budgetDynamics "Расчет динамики бюджета"
            autoLayout
        }

        systemContext budgetingApp "BudgetingSystem" {
            include *
            autoLayout
        }

        container budgetingApp {
            include *
            autoLayout
        }
    }
}