from rest_framework import viewsets, permissions, generics
from .serializers import UserSerializer, GroupSerializer, BoardSerializer, CellSerializer
from django.contrib.auth.models import User, Group
from .models import Board, Cell

#-------------------------------------------------------------------------------
class BoardUpdate(generics.ListAPIView):
    """
    Board update

    Called by REST query:
    http://127.0.0.1:8000/cells_from/?board_id=<board_id>&cmd=update&cell_name=<cell_name>
    curl -H 'Accept: application/json; indent=4' -u admin:adminadmin url http://127.0.0.1:8000/cells_from/?board_id=19&cmd=update&cell_name=4_5
    """
    serializer_class = CellSerializer

    def get_queryset(self):
        """
        Sends the update message to the model
        Returns to caller a filtered list of Cells.
        Update game 
        """
        queryset = Cell.objects.all()
        board_id = self.request.query_params.get('board_id', None)
        cell_name = self.request.query_params.get('cell_name', None)
        flag = self.request.query_params.get('flag', None)
        if board_id is not None:
            board = Board.objects.get(id=board_id)
            queryset = queryset.filter(board=board_id)
        if (cell_name is not None) and (flag is not None):
            try:
                board.update_game(cell_name, flag)
            except TransitionNotAllowed:
                print('ERROR')
            else:
                pass
        return queryset

class BoardInit(generics.ListAPIView):
    """
    Board init
    """
    serializer_class = BoardSerializer
    def get_queryset(self):
        queryset = Board.objects.all()
        board_id = self.request.query_params.get('board_id', None)
        if board_id is not None:
            board = Board.objects.get(id=board_id)
            board.init_game()
            queryset = queryset.filter(id=board_id)
        return queryset

class BoardCheck(generics.ListAPIView):
    """
    Board check
    """
    serializer_class = BoardSerializer
    def get_queryset(self):
        queryset = Board.objects.all()
        board_id = self.request.query_params.get('board_id', None)
        cell_name = self.request.query_params.get('cell_name', None)
        if board_id is not None:
            board = Board.objects.get(id=board_id)
            queryset = queryset.filter(id=board_id)
        board.check_game(cell_name)
        return queryset

#-------------------------------------------------------------------------------
class CellViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cells to be viewed or edited.
    """
    queryset = Cell.objects.all().order_by('-name')
    serializer_class = CellSerializer
    #permission_classes = [permissions.IsAuthenticated]

class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Boards to be viewed or edited.
    """
    queryset = Board.objects.all().order_by('name')
    serializer_class = BoardSerializer
    #permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]

#class GroupViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows groups to be viewed or edited.
#    """
#    queryset = Group.objects.all()
#    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]
