import unittest
import torch

from routeml.utils import get_graph_embedding  

class TestGraphEmbedding(unittest.TestCase):
    
    def setUp(self):
        self.batch_size = 4
        self.seq_length = 5
        self.node_emb_size = 6

    def test_graph_embedding_shape(self):
        src_key_padding_mask = torch.randint(0, 2, (self.batch_size, self.seq_length), dtype=torch.bool)
        node_emb = torch.randn(self.batch_size, self.seq_length, self.node_emb_size)
        output = get_graph_embedding(src_key_padding_mask, node_emb)
        self.assertEqual(output.shape, (self.batch_size, self.node_emb_size))

    def test_graph_embedding_zero_mask(self):
        src_key_padding_mask = torch.zeros(self.batch_size, self.seq_length, dtype=torch.bool)
        node_emb = torch.randn(self.batch_size, self.seq_length, self.node_emb_size)
        output = get_graph_embedding(src_key_padding_mask, node_emb)
        self.assertTrue(torch.equal(output, node_emb.sum(dim=1) / self.seq_length))

    def test_graph_embedding_one_mask(self):
        src_key_padding_mask = torch.ones(self.batch_size, self.seq_length, dtype=torch.bool)
        node_emb = torch.randn(self.batch_size, self.seq_length, self.node_emb_size)
        with self.assertRaises(ValueError) as context:
            get_graph_embedding(src_key_padding_mask, node_emb)
        self.assertEqual(str(context.exception), "The src_key_padding_mask cannot be all 1s.")
