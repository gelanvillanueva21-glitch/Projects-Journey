


interface Employee {
    id: number;
    fullName: string;
    email: string;
    department: "engineering" | "design" | "marketing";
    salary: number;
    isActive: boolean;
    accessToken: string;
}


type EmployeeCardsProps = Pick<Employee,    "fullName" | "department" | "isActive">
type EmployeeUpdateForm = Partial<Employee>
type PublickEmployee = Omit<Employee, "accessToken" | "salary">


type BooleanFlags<T> = {
    [K in keyof T]: boolean
}


type DepartmentConfig = Record<Employee["department"], {head: string; budget: number}>


function createEmployeeCardData(employee: Employee): EmployeeCardsProps{
    return {
        fullName: employee.fullName,
        department: employee.department,
        isActive: employee.isActive
    }
}


function isEmployeeActive(flags: BooleanFlags<Employee>): boolean{
    return flags.isActive
}



const employee: Employee = {
    id: 1,
    fullName: "John Kent",
    email: "johnkenet@gmail.com",
    department: "engineering",
    salary: 150000,
    isActive: true,
    accessToken: "sahjdh812yhfah1",
};


console.log(createEmployeeCardData(employee));


const flags: BooleanFlags<Employee> = {
    id: true,
    fullName: false,
    email: true,
    department: false,
    salary: true,
    isActive: true,
    accessToken: false,
}


console.log(isEmployeeActive(flags));



