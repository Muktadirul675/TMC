var sidebar_open = false

const toggle_sidebar = () => {
    if(sidebar_open){
        sidebar_open = false;
        $("#blog_side_bar").toggleCLass('col-2');
    }
}
