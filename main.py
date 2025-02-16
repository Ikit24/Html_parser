from textnode import TextNode, TextType

def main():
    node = TextNode("This is a link", TextType.LINK, "https://www.geeksforgeeks.org/python-main-function/")

    print(node)

if __name__=="__main__":
    main()
