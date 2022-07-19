	std::vector<Vec2> pointsToInsert;
	pointsToInsert.insert(pointsToInsert.end(), convexPoly.m_vertexes.begin(), convexPoly.m_vertexes.end());
	pointsToInsert.insert(pointsToInsert.end(), artificialPoints.begin(), artificialPoints.end());

	int maxLoops = (maxSteps == -1) ? (int)pointsToInsert.size() : maxSteps; // Debug Stepping the triangulation

	std::vector<DelaunayTriangle> badTriangles;
	for (int vertexIndex = 0; vertexIndex < maxLoops; vertexIndex++) {
		std::vector<DelaunayEdge> allEdges; // Contains all edges used so far
		std::vector<DelaunayEdge> badEdges; // Contains edges shared by bad triangles

		Vec2 const& vertex = pointsToInsert[vertexIndex];

		for (std::vector<DelaunayTriangle>::iterator triangleIt; triangleIt != calculatedTriangles.end(); ) {
			DelaunayTriangle& triangle = *triangleIt;
			if (triangle.IsPointAVertex(vertex)) continue;

			if (triangle.IsPointInsideCircumcenter(vertex)) {
				badTriangles.push_back(triangle);
				DelaunayEdge triangleEdges[3];
				triangle.GetEdges(triangleEdges);

				for (int edgeIndex = 0; edgeIndex < 3; edgeIndex++) {
					if (std::find(allEdges.begin(), allEdges.end(), triangleEdges[edgeIndex]) != allEdges.end()) { // If other triangles shares this edge, it's a bad edge
						badEdges.push_back(triangleEdges[edgeIndex]);
					}
					else {
						allEdges.push_back(triangleEdges[edgeIndex]);
					}
				}

				triangleIt = calculatedTriangles.erase(triangleIt);
			}
			else {
				triangleIt++;
			}

		}

		// Create subsequent triangles
		for (int edgeIndex = 0; edgeIndex < allEdges.size(); edgeIndex++) {
			DelaunayEdge const& edge = allEdges[edgeIndex];

			if (std::find(badEdges.begin(), badEdges.end(), allEdges[edgeIndex]) == badEdges.end()) {
				bool areSomeVertexEqual = (edge.m_pointA - edge.m_pointB).GetLengthSquared() < toleranceVertexDistance;
				areSomeVertexEqual = areSomeVertexEqual || ((edge.m_pointA - vertex).GetLengthSquared() < toleranceVertexDistance);
				areSomeVertexEqual = areSomeVertexEqual || ((edge.m_pointB - vertex).GetLengthSquared() < toleranceVertexDistance);
				if (!areSomeVertexEqual) {
					DelaunayTriangle newTriangle(edge.m_pointA, edge.m_pointB, vertex);
					if (newTriangle.IsTriangleCollapsed()) continue; // Warning. Collapsed triangles are common in this algorithm. It's a question of how collapsed I allow it to be
					auto it = std::find(badTriangles.begin(), badTriangles.end(), newTriangle);

					if (it == badTriangles.end()) {
						calculatedTriangles.emplace_back(edge.m_pointA, edge.m_pointB, vertex);
					}

				}
			}
		}
	}
