export const menuList = [
    {
      menuname: "Dashboard",
      icon: "bi bi-grid",
      routepath: "/",
    },
    {
      menuname: "AWS Accounts",
      icon: "bi bi-clouds",
      submenu: [
        {
          menuname: "Add Account",
          routepath: "/aws/add-account",
        },
        {
          menuname: "List Accounts",
          routepath: "/aws/accounts",
        }, 
        {
          menuname: "Edit Account",
          routepath: "/aws/edit-account",
        },        
      ],
    },
    {
      menuname: "RDS Instances",
      icon: "bi bi-database",
      submenu: [
        {
          menuname: "Browse RDS Instances",
          routepath: "/aws/rds/browse",
        },
        {
          menuname: "List RDS Instances",
          routepath: "/aws/rds/list-rds",
        },
        {
          menuname: "View RDS Detail",
          routepath: "/aws/rds/view-rds",
        },        
      ],
    },   
    {
      menuname: "RDS EOL",
      icon: "bi bi-align-end",
      submenu: [
        {
          menuname: "RDS Postgres",
          routepath: "/aws/rds/eol/pg",
        },
        {
          menuname: "RDS Aurora Postgres",
          routepath: "/aws/rds/eol/apg",
        },  
        {
          menuname: "RDS MySQL",
          routepath: "/aws/rds/eol/mysql",
        },
        {
          menuname: "RDS Aurora MySQL",
          routepath: "/aws/rds/eol/amysql",
        },      
      ],
    },  
    {
      menuname: "RDS Types(H/W)",
      icon: "bi bi-motherboard",
      submenu: [
        {
          menuname: "RDS EBS instance types",
          routepath: "/aws/rds/hw/ebs",
        },
        {
          menuname: "RDS instance types",
          routepath: "/aws/rds/hw/rds",
        },       
      ],
    }, 
    {   
      menuname: "Provision Database",
      icon: "bi bi-kanban-fill",
      submenu: [
        {
          menuname: "Create Jira Meta",
          routepath: "/jira/meta/create",
        },
        {
          menuname: "List Jira Meta",
          routepath: "/jira/meta/list",
        },   
        {
          menuname: "Edit Jira Meta",
          routepath: "/jira/meta/edit-m",
        },  
        {
          menuname: "Create Server Meta",
          routepath: "/msserver/meta/create",
        },           
        {
          menuname: "List Server Meta",
          routepath: "/msserver/meta/list",
        }, 
        {
          menuname: "View Server Meta",
          routepath: "/msserver/meta/view-ser",
        },  
        {
          menuname: "Edit Server Meta",
          routepath: "/msserver/meta/edit-ser",
        },                
        {
          menuname: "Provision Database",
          routepath: "/msserver/provision/mssql/database",
        },    
        {
          menuname: "List Provision Jobs",
          routepath: "/provision/database/jobs",
        },    
        {
          menuname: "View Job Details",
          routepath: "/provision/database/view-job",
        },                                   
      ],
    },          
    {
      menuname: "Users",
      icon: "bi bi-people",
      submenu: [
        {
          menuname: "List Users",
          routepath: "/account/listallusers",
        },
        {
          menuname: "Add Users",
          routepath: "/account/adduser",
        },
        {
          menuname: "Edit User",
          routepath: "/account/edit-user",
        },            
        {
          menuname: "Profile",
          routepath: "/account/profile",
        },
      ],
    },
  ];  