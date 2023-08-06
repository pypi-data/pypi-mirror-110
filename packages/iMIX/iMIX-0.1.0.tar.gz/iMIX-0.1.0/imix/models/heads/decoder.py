import torch
import torch.nn as nn

from imix.models.encoder.visdiag_lstm import DynamicRNN
from ..builder import HEADS
import json


@HEADS.register_module()
class VISDIALPRINCIPLES_HEAD(nn.Module):

    def __init__(self, decoder_type, **kwargs):
        super().__init__()
        if decoder_type == 'disc_by_round':
            self.model = Disc_by_round_Decoder(**kwargs)

        elif decoder_type == 'disc_qt':
            self.model = Disc_qt_Decoder(**kwargs)

    def forward(self, encoder_output, data):
        return self.model(encoder_output, data)


class Disc_qt_Decoder(nn.Module):

    def __init__(self, config, vocabulary):
        super().__init__()
        self.config = config
        self.nhid = config['lstm_hidden_size']

        self.word_embed = nn.Embedding(
            len(vocabulary),
            config['word_embedding_size'],
            padding_idx=vocabulary.PAD_INDEX,
        )
        self.option_rnn = nn.LSTM(
            config['word_embedding_size'],
            config['lstm_hidden_size'],
            config['lstm_num_layers'],
            batch_first=True,
            dropout=config['dropout'],
        )
        self.a2a = nn.Linear(self.nhid * 2, self.nhid)
        self.option_rnn = DynamicRNN(self.option_rnn)
        path = 'data/qt_scores.json'
        file = open(path, 'r')
        self.count_dict = json.loads(file.read())
        file.close()
        file = open('data/qt_count.json', 'r')
        self.qt_file = json.loads(file.read())
        self.qt_list = list(self.qt_file.keys())
        file.close()

    def forward(self, encoder_output, batch):
        """Given `encoder_output` + candidate option sequences, predict a score
        for each option sequence.

        Parameters
        ----------
        encoder_output: torch.Tensor
            Output from the encoder through its forward pass.
            (batch_size, num_rounds, lstm_hidden_size)
        """

        options = batch['opt']
        batch_size, num_options, max_sequence_length = options.size()
        options = options.contiguous().view(-1, max_sequence_length)

        options_length = batch['opt_len']
        options_length = options_length.contiguous().view(-1)

        options_embed = self.word_embed(options)  # b*100 20 300
        _, (options_feat, _) = self.option_rnn(options_embed, options_length)  # b*100 512
        options_feat = options_feat.view(batch_size, num_options, self.nhid)

        encoder_output = encoder_output.unsqueeze(1).repeat(1, num_options, 1)

        scores = torch.sum(options_feat * encoder_output, -1)
        scores = scores.view(batch_size, num_options)

        qt_score = torch.zeros_like(scores)
        qt_idx = batch['qt']
        opt_idx = batch['opt_idx']
        for b in range(batch_size):
            qt_key = self.qt_list[qt_idx[b]]
            ans_relevance = self.count_dict[qt_key]
            for k in range(100):
                idx_temp = str(opt_idx[b][k].detach().cpu().numpy())
                if idx_temp in ans_relevance.keys():
                    qt_score[b][k] = 1

        return scores, qt_score


class Disc_by_round_Decoder(nn.Module):

    def __init__(self, vocabulary_len, word_embedding_size, lstm_hidden_size, lstm_num_layers, dropout):
        super().__init__()

        self.nhid = lstm_hidden_size

        self.word_embed = nn.Embedding(vocabulary_len, word_embedding_size, padding_idx=0)
        self.option_rnn = nn.LSTM(
            word_embedding_size,
            lstm_hidden_size,
            lstm_num_layers,
            batch_first=True,
            dropout=dropout,
        )
        self.a2a = nn.Linear(self.nhid * 2, self.nhid)  # this is useless in this version
        # Options are variable length padded sequences, use DynamicRNN.
        self.option_rnn = DynamicRNN(self.option_rnn)

    def forward(self, encoder_output, data):
        """Given `encoder_output` + candidate option sequences, predict a score
        for each option sequence.

        Parameters
        ----------
        encoder_output: torch.Tensor
            Output from the encoder through its forward pass.
            (batch_size, num_rounds, lstm_hidden_size)
        """
        options = data['opt']
        batch_size, num_options, max_sequence_length = options.size()
        options = options.contiguous().view(-1, max_sequence_length)

        options_length = data['opt_len']
        options_length = options_length.contiguous().view(-1)

        options_embed = self.word_embed(options)  # b*100 20 300
        _, (options_feat, _) = self.option_rnn(options_embed, options_length)  # b*100 512
        options_feat = options_feat.view(batch_size, num_options, self.nhid)

        encoder_output = encoder_output.unsqueeze(1).repeat(1, num_options, 1)
        scores = torch.sum(options_feat * encoder_output, -1)
        scores = scores.view(batch_size, num_options)

        return scores
