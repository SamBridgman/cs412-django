from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from .models import Voter
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline
from django.db.models.functions import ExtractYear
from urllib.parse import quote


# View for displaying paginated list of voters with optional filtering
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        voted_previous = self.request.GET.get('voted_previous')
        
        # apply filters if they exist
        if party:
            queryset = queryset.filter(party_affiliation=party)
        
        if min_dob:
            queryset = queryset.filter(date_of_birth__year__gte=min_dob)
        
        if max_dob:
            queryset = queryset.filter(date_of_birth__year__lte=max_dob)
        
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
            
        if voted_previous:
            # if they voted in the previous election
            queryset = queryset.filter(
                Q(v20state=True) |
                Q(v21town=True) |
                Q(v21primary=True) |
                Q(v22general=True) |
                Q(v23town=True)
            )
        
        return queryset


# View for displaying graphs and analytics of voter data
class VoterGraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        voted_previous = self.request.GET.get('voted_previous')
        
        # apply filters if they exist
        if party:
            queryset = queryset.filter(party_affiliation=party)
        
        if min_dob:
            queryset = queryset.filter(date_of_birth__year__gte=min_dob)
        
        if max_dob:
            queryset = queryset.filter(date_of_birth__year__lte=max_dob)
        
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
            
        if voted_previous:
            # if they voted in the previous election
            queryset = queryset.filter(
                Q(v20state=True) |
                Q(v21town=True) |
                Q(v21primary=True) |
                Q(v22general=True) |
                Q(v23town=True)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        """Gets context data for template, including voter distribution graphs"""
        context = super().get_context_data(**kwargs)
        filtered_voters = self.get_queryset()
        
        # Party Affiliation Distribution
        party_counts = filtered_voters.values('party_affiliation').annotate(count=Count('voter_id'))
        party_fig = go.Pie(
            labels=[p['party_affiliation'] for p in party_counts],
            values=[p['count'] for p in party_counts]
        )
        party_graph = plotly.offline.plot(
            {"data": [party_fig], "layout_title_text": "Distribution of Party Affiliations"},
            auto_open=False,
            output_type="div"
        )
        context['party_graph'] = party_graph

        # Voter Age Distribution
        birth_years = filtered_voters.annotate(year=ExtractYear('date_of_birth')).values('year').annotate(count=Count('voter_id'))
        age_fig = go.Bar(
            x=[y['year'] for y in birth_years],
            y=[y['count'] for y in birth_years]
        )
        age_graph = plotly.offline.plot(
            {
                "data": [age_fig],
                "layout_title_text": "Distribution of Voter Birth Years",
                "layout_xaxis_title": "Birth Year",
                "layout_yaxis_title": "Number of Voters"
            },
            auto_open=False,
            output_type="div"
        )
        context['age_graph'] = age_graph

        # Voter Score Distribution
        score_counts = filtered_voters.values('voter_score').annotate(count=Count('voter_id'))
        score_fig = go.Bar(
            x=[s['voter_score'] for s in score_counts if s['voter_score'] is not None],
            y=[s['count'] for s in score_counts if s['voter_score'] is not None]
        )
        score_graph = plotly.offline.plot(
            {
                "data": [score_fig],
                "layout_title_text": "Distribution of Voter Scores",
                "layout_xaxis_title": "Voter Score",
                "layout_yaxis_title": "Number of Voters"
            },
            auto_open=False,
            output_type="div"
        )
        context['score_graph'] = score_graph

        # Voting History
        voting_history = {
            '2020 State': filtered_voters.filter(v20state=True).count(),
            '2021 Town': filtered_voters.filter(v21town=True).count(),
            '2021 Primary': filtered_voters.filter(v21primary=True).count(),
            '2022 General': filtered_voters.filter(v22general=True).count(),
            '2023 Town': filtered_voters.filter(v23town=True).count()
        }
        
        voting_fig = go.Bar(
            x=list(voting_history.keys()),
            y=list(voting_history.values()),
            text=list(voting_history.values()),
            textposition='auto'
        )
        voting_graph = plotly.offline.plot(
            {
                "data": [voting_fig],
                "layout_title_text": "Voting History by Election",
                "layout_xaxis_title": "Election",
                "layout_yaxis_title": "Number of Voters"
            },
            auto_open=False,
            output_type="div"
        )
        context['voting_graph'] = voting_graph

        return context


# View for displaying individual voter details including a Google Maps link to their address
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voter = self.get_object()
        
        # create google maps url
        address = f"{voter.street_number} {voter.street_name}"
        if voter.apartment_number:
            address += f" {voter.apartment_number}"
        address += f", {voter.zip_code}"
        
        encoded_address = quote(address)
        context['google_maps_url'] = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"
        
        return context
