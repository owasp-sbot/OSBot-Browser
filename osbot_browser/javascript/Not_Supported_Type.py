from osbot_browser.javascript.Base_Node import Base_Node



class Not_Supported_Type(Base_Node):
    def parse_node(self):
        from osbot_browser.javascript.Globals import NOT_SUPPORTED_TYPE
        self.node_type = f"{NOT_SUPPORTED_TYPE} : {self.node_type}"
        print(f"***** {self.node_type}")