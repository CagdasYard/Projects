from PIL import Image, ImageDraw, ImageFont

PrefixVisualTreeDictionary = {}
Font = ImageFont.truetype("comic.ttf", 36)

class Tracker: 
    def __init__(self, function): 
        self.function = function 
        self.Call = 0
    
    def __call__(self, *args, **kwargs): 

        self.Call += 1
        result = self.function(*args, **kwargs)
        return result

def ConnectNodesToRoots(PrefixNode):
    if PrefixNode.Left == None and PrefixNode.Right == None:
        return
    
    if PrefixNode.Left != None:
        PrefixNode.Left.Root = PrefixNode
        
    if PrefixNode.Right != None:
        PrefixNode.Right.Root = PrefixNode

    ConnectNodesToRoots(PrefixNode.Left)
    ConnectNodesToRoots(PrefixNode.Right)    

class Node:
    def __init__(self,Value,Left=None,Right=None,Root=None):
        self.Value = Value
        self.Left  = Left
        self.Right = Right
        self.Root  = Root
            
def StringPrefix(PrefixNode):
    if PrefixNode.Right == None and PrefixNode.Left == None:
        return PrefixNode.Value
    elif PrefixNode.Value in ["+","-","*","/","^"]:
        Left = StringPrefix(PrefixNode.Left)
        Right = StringPrefix(PrefixNode.Right)
        return " ".join([PrefixNode.Value,Left,Right])
    else:
        return

def BinaryTreeLevel(BinaryNode, CurrentLevel=0):
    if BinaryNode.Right == None and BinaryNode.Left == None:
        return CurrentLevel
    Left = BinaryTreeLevel(BinaryNode.Left, CurrentLevel + 1)
    Right = BinaryTreeLevel(BinaryNode.Right, CurrentLevel + 1)

    return Left if Left > Right else Right

def FiilVisualTreeDictionary(PrefixNode, Level=0):
    global PrefixVisualTreeDictionary
    if PrefixNode.Left == None and PrefixNode.Right == None:
        FontSize = Font.getsize(PrefixNode.Value)
        PrefixVisualTreeDictionary[PrefixNode] = [[0,0], FontSize, Level]
        return 

    if PrefixNode not in PrefixVisualTreeDictionary:
        FontSize = Font.getsize(PrefixNode.Value)
        PrefixVisualTreeDictionary[PrefixNode] = [[0,0], FontSize, Level]
    FiilVisualTreeDictionary(PrefixNode.Left, Level+1)
    FiilVisualTreeDictionary(PrefixNode.Right, Level+1)        

def SetVisualTreeCoordinates(PrefixNode, Level, Coordinates=[0,0], UnitWidth=50, UnitHeight=80):

    if PrefixNode.Left == None and PrefixNode.Right == None:
        FontSize = Font.getsize(PrefixNode.Value)
        PrefixVisualTreeDictionary[PrefixNode][0] = Coordinates
        return
    PrefixVisualTreeDictionary[PrefixNode][0] = Coordinates
    SetVisualTreeCoordinates(PrefixNode.Left,  Level-1, [Coordinates[0] - UnitWidth * (2 ** (Level - 1)), Coordinates[1] + UnitHeight], UnitWidth, UnitHeight)
    SetVisualTreeCoordinates(PrefixNode.Right, Level-1, [Coordinates[0] + UnitWidth * (2 ** (Level - 1)), Coordinates[1] + UnitHeight], UnitWidth, UnitHeight)

def ShiftVisualTreeNodes(PrefixNode, UnitWidth=50, UnitHeight=80):
    MaxLevel = max(Info[2] for Info in PrefixVisualTreeDictionary.values())

    for Level in reversed(range(MaxLevel + 1)):
        Queue = [Info for Info in PrefixVisualTreeDictionary.values() if Info[2] == Level]
        Keys  = [Item[0] for Item in PrefixVisualTreeDictionary.items() if Item[1][2] == Level]
        
        for Index in range(len(Queue)):
            Node = Queue[Index]
            X = Node[0][0] - Node[1][0] // 2
            Y = Node[0][1] - Node[1][1] // 2
            Queue[Index][0] = [X,Y]
        
        for Index in range(len(Queue)-1):
            CurrentNode = Queue[Index]
            CurrentRightEdge = CurrentNode[0][0] + CurrentNode[1][0] 

            NextNode = Queue[Index + 1]
            NextLeftEdge = NextNode[0][0]

            Distance = NextLeftEdge - CurrentRightEdge
            if Distance < UnitWidth * 2 ** (MaxLevel + 1 - Level):                    
                Shift = UnitWidth * 2 ** (MaxLevel + 1 - Level) - NextLeftEdge + CurrentRightEdge

                if Keys[Index].Right != None and Keys[Index + 1].Left != None:
                    CurrentLeftChild = Keys[Index].Right
                    NextRightChild = Keys[Index + 1].Left

                    LeftChildInfo = PrefixVisualTreeDictionary[CurrentLeftChild]
                    RightChildInfo = PrefixVisualTreeDictionary[NextRightChild]

                    LeftChildRightEdge = LeftChildInfo[0][0] + LeftChildInfo[1][0] 
                    RightChildLeftEdge = RightChildInfo[0][0]

                    Shift += UnitWidth * 2 ** (MaxLevel - Level-1) - RightChildLeftEdge + LeftChildRightEdge

                Queue[Index + 1][0][0] += Shift
                ShiftRoots(Keys[Index + 1], Shift // 2)
                if Keys[Index + 1].Right != None:
                    NextRight = Keys[Index + 1].Right
                    ShiftChildren(NextRight, Shift)

                if Keys[Index + 1].Left != None:
                    NextLeft = Keys[Index + 1].Left
                    ShiftChildren(NextLeft, Shift)
                    
    LeftEdge = -1 * min((Info[0][0] for Info in PrefixVisualTreeDictionary.values()))
    TopEdge = -1 * min((Info[0][1] for Info in PrefixVisualTreeDictionary.values()))
    for Node, Info in PrefixVisualTreeDictionary.items():
        Info[0][0] += LeftEdge + UnitWidth // 2
        Info[0][1] += TopEdge + UnitHeight // 2

def ShiftRoots(PrefixNode, Shift):
    if PrefixNode.Root == None:
        PrefixVisualTreeDictionary[PrefixNode][0][0] += Shift
        return

    ShiftRoots(PrefixNode.Root,Shift // 2)
    PrefixVisualTreeDictionary[PrefixNode.Root][0][0] += Shift

def ShiftChildren(PrefixNode, Shift):
    if PrefixNode.Left == None and PrefixNode.Right == None:
        PrefixVisualTreeDictionary[PrefixNode][0][0] += Shift
        return
    ShiftChildren(PrefixNode.Left, Shift)
    ShiftChildren(PrefixNode.Right, Shift)    
    if PrefixNode.Left != None:
        PrefixVisualTreeDictionary[PrefixNode.Left][0][0] += Shift
    if PrefixNode.Right != None:
        PrefixVisualTreeDictionary[PrefixNode.Right][0][0] += Shift        

def DrawPrefixTree(PrefixNode, UnitWidth=50, UnitHeight=80):

    RightEdge = UnitWidth  + max(Info[0][0]+Info[1][0] for Info in PrefixVisualTreeDictionary.values())
    BottomEdge = UnitHeight + max(Info[0][1] for Info in PrefixVisualTreeDictionary.values())

    Level = BinaryTreeLevel(PrefixNode)
    Sizes = RightEdge, BottomEdge

    Picture = Image.new("RGBA", Sizes, (0, 0, 0, 0))
    Draw = ImageDraw.Draw(Picture)
    Font = ImageFont.truetype("comic.ttf", 36)
    Draw.rectangle([(0,0),Sizes],fill= (0,0,0))
    
    for Nodes,Info in PrefixVisualTreeDictionary.items():

        LowerRightCorner = (Info[0][0] + Info[1][0] + 5, Info[0][1] + Info[1][1] + 5)
        Draw.rectangle([(Info[0][0] - 5, Info[0][1] + 5), LowerRightCorner],width = 4)
        Draw.text(Info[0], Nodes.Value, font=Font, fill=(255,255,255))
        MiddleY = Info[0][1] + Info[1][1] // 2 + 4
        
        if Nodes.Left != None:
            LeftInfo = PrefixVisualTreeDictionary[Nodes.Left]
            LeftCenter = LeftInfo[0][0] + LeftInfo[1][0] // 2
            LeftEdge = Info[0][0] - 4

            Draw.line((LeftCenter, MiddleY, LeftCenter, LeftInfo[0][1] + 4), width=4)        
            Draw.line((LeftCenter, MiddleY, LeftEdge, MiddleY), width=4)

            
        if Nodes.Right != None:
            RightInfo = PrefixVisualTreeDictionary[Nodes.Right]
            RightCenter = RightInfo[0][0] + RightInfo[1][0] // 2
            RightEdge = Info[0][0] + Info[1][0] + 4

            Draw.line((RightCenter, MiddleY, RightCenter, RightInfo[0][1] + 4), width=4)
            Draw.line((RightCenter, MiddleY, RightEdge, MiddleY), width=4)


    Picture.show()

def PrefixVisualisation(PrefixNode, UnitWidth=50, UnitHeight=80):
    FiilVisualTreeDictionary(PrefixNode)
    MaxLevel = BinaryTreeLevel(PrefixNode)
    SetVisualTreeCoordinates(PrefixNode, MaxLevel, UnitWidth=UnitWidth, UnitHeight=UnitHeight)
    ShiftVisualTreeNodes(PrefixNode, UnitWidth=UnitWidth, UnitHeight=UnitHeight)    
    DrawPrefixTree(PrefixNode, UnitWidth=UnitWidth, UnitHeight=UnitHeight)
    
@Tracker    
def Prefix(Stack):
    
    PMOperators = [[Item,Index,False] for Index,Item in enumerate(Stack) if Item in ["+","-"]]
    MDOperators = [[Item,Index,False] for Index,Item in enumerate(Stack) if Item in ["*","/"]]
    EOperators  = [[Item,Index,False] for Index,Item in enumerate(Stack) if Item == "^"]
    
    if not any([PMOperators,MDOperators,EOperators]):
        return Node("".join(Stack))

    Parentesis = [(Item,Index) for Index,Item in enumerate(Stack) if Item in ["(",")"]]

    ParentesisLevel = 0
    OpenParentesis = 0
    CloseParentesis = 0

    Parentheses = []

    for Item,Index in Parentesis:
        if Item == "(":
            if not bool(ParentesisLevel):
                OpenParentesis = Index
            ParentesisLevel += 1
        elif Item == ")":
            ParentesisLevel -= 1
            if not bool(ParentesisLevel):
                CloseParentesis = Index
                Parentheses.append((OpenParentesis,CloseParentesis))
            
    for PM in PMOperators:
        for Brackets in Parentheses:
            if PM[1] in range(Brackets[0] + 1,Brackets[1]):
                PM[2] = True
                break
    for MD in MDOperators:
        for Brackets in Parentheses:
            if MD[1] in range(Brackets[0] + 1,Brackets[1]):
                MD[2] = True
                break
    for E in EOperators:
        for Brackets in Parentheses:
            if E[1] in range(Brackets[0] + 1,Brackets[1]):
                E[2] = True
                break

    PMOperators = [PM for PM in PMOperators if not PM[2]]
    MDOperators = [MD for MD in MDOperators if not MD[2]]
    EOperators  = [E for E in EOperators if not E[2]]

    if PMOperators:
        Item,Index = PMOperators[-1][:2]
        Left = Prefix(Stack[:Index])
        Right = Prefix(Stack[Index+1:])
        return Node(Item,Left,Right)
    
    elif MDOperators:
        Item,Index = MDOperators[-1][:2]
        Left = Prefix(Stack[:Index])
        Right = Prefix(Stack[Index + 1:])
        return Node(Item,Left,Right)         

    elif EOperators:
        Item,Index = EOperators[-1][:2]
        Left = Prefix(Stack[:Index])
        Right = Prefix(Stack[Index + 1:])
        return Node(Item,Left,Right)

    if Parentheses:

        return Prefix(Stack[Parentheses[-1][0] + 1:Parentheses[-1][1]])
        
String = input()
Stack = []
Sub = []
for Item in list(String):
    if Item == " ":
        continue
    if Item.isnumeric() or Item == ".":
        Sub.append(Item)
    if Item in ["(",")","+","-","/","^","*"]:
        if Sub:
            Stack.append("".join(Sub))
            Sub.clear()    
        Stack.append(Item)
if Sub:
    Stack.append("".join(Sub))
    Sub.clear()
Converted = Prefix(Stack)
ConvertedString = StringPrefix(Converted)
ConnectNodesToRoots(Converted)

print(ConvertedString)
PrefixVisualisation(Converted, UnitWidth=20, UnitHeight=100)

