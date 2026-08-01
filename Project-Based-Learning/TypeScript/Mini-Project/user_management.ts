


interface Employee {
    id: number;
    fullname: string;
    email: string;
    department: "engineering" | "design" | "marketing";
    salary: number;
    isActive: boolean;
    accessToken: string;
}


type EmployeeCardsProps = Pick<Employee, "fullname" | "department" | "isActive">
type EmployeeUpdateForm = Partial<Employee>
type PublickEmployee = Omit<Employee, "accessToken" | "salary">


type BooleanFlags<T> = {
    id: boolean;
    fullname: boolean;
    email: boolean;
    department: boolean;
    salary: boolean;
    isActive: boolean;
    accessToken: boolean;
}


type DepartmentConfig = Record<Employee["department"], {head: string; budget: number}>


function createEmployeeCardDate(employee: Employee): EmployeeCardsProps{
    return employee
}


function isEmployeeActive(flags: BooleanFlags<Employee>): boolean{
    return flags.isActive
}



const employee: Employee = {
    id: 1,
    fullname: "John Kent",
    email: "johnkenet@gmail.com",
    department: "engineering",
    salary: 150000,
    isActive: true,
    accessToken: "sahjdh812yhfah1",
};


console.log(createEmployeeCardDate(employee));


const flags: BooleanFlags<Employee> = {
    id: true,
    fullname: false,
    email: true,
    department: false,
    salary: true,
    isActive: true,
    accessToken: false,
}


console.log(isEmployeeActive(flags));



