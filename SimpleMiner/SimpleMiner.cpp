// Creates a vector that contains the offsets for rendering chunks
// to get the correct water effect. (Render chunks farther away first to blend correctly with water textures)

void World::CalulateRenderingOrder()
{
	int maxChunkRadiusX = 1 + int(m_activationRange) / CHUNK_SIZE_X;
	int maxChunkRadiusY = 1 + int(m_activationRange) / CHUNK_SIZE_Y;

	for (int xOffset = -maxChunkRadiusX; xOffset < maxChunkRadiusX; xOffset++) {
		for (int yOffset = -maxChunkRadiusY; yOffset < maxChunkRadiusY; yOffset++) {
			IntVec2 offset(xOffset, yOffset);
			m_orderedRenderingOffsets.push_back(offset); // Vector
		}
	}

	std::sort(m_orderedRenderingOffsets.begin(), m_orderedRenderingOffsets.end(), [](IntVec2 const& left, IntVec2 const& right){
		int leftSum = abs(left.x) + abs(left.y);
		int rightSum = abs(right.x) + abs(right.y);

		return leftSum < rightSum;
	});

   // Reverse, to access in desired order
	std::reverse(m_orderedRenderingOffsets.begin(), m_orderedRenderingOffsets.end());
}
